#include <pybind11/pybind11.h>
#include "../include/ComponentTree.hpp"
#include "../include/NodeCT.hpp"
#include "../include/AttributeComputedIncrementally.hpp"

#include <vector>

namespace py = pybind11;

#ifndef COMPUTER_DERIVATIVE_H
#define COMPUTER_DERIVATIVE_H


class ComputerDerivatives {
    
    private:
        

    public:
        ComputerDerivatives();

        py::tuple derivadaOutput_thetas(py::array_t<float> &attributes, std::vector<float> sigmoid, std::vector<int> h, std::vector<int> listIdsNodes, std::vector<int> listIdsParent);
        
        void derivadaOutputThetas(ComponentTree* tree, float* attrs, std::vector<float> sigmoid, float *dWeight, float *dBias, int rows, int cols);
        
        py::tuple derivadaLoss_thetas(ComponentTree* tree, py::array_t<float> &attrs, std::vector<float> sigmoid, py::array_t<float> gradientOfLoss) ;

        static py::tuple gradients(ComponentTree* tree, py::array_t<float> &attrs, std::vector<float> sigmoid, py::array_t<float> gradientOfLoss) {
            auto buf_attrs = attrs.request();
            float* attributes = (float *) buf_attrs.ptr;
            int rows = buf_attrs.shape[0];
            int cols = buf_attrs.shape[1];
            
            float *dWeight = new float[rows * cols];
            float *dBias = new float[rows];
            for(NodeCT* node: tree->getListNodes()){
                int id = node->getIndex();
                dBias[id] = (sigmoid[id] * (1 - sigmoid[id])) * node->getResidue();
                for (int j = 0; j < cols; j++)
                    dWeight[id + (rows * j)] = (sigmoid[id] * (1 - sigmoid[id])) * attributes[id + (rows * j)] * node->getResidue();

                if (id > 0) {
                    int idParent = node->getParent()->getIndex();
                    dBias[id] += dBias[idParent];
                    for (int j = 0; j < cols; j++)
                        dWeight[id + (rows * j)] += dWeight[idParent + rows * j];
                }
            }


            auto buf_gradLoss = gradientOfLoss.request();
            float* gradLoss = (float *) buf_gradLoss.ptr;
            
            float *gradWeight = new float[cols];
            float *gradBias = new float[1];
            gradBias[0] = 0;
            for (int j = 0; j < cols; j++)
                gradWeight[j] = 0;
            

            float *summationGrad = new float[tree->getNumNodes()];
            float *gradInput = new float[tree->getNumRowsOfImage() * tree->getNumColsOfImage()];
            AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
                    [&summationGrad, &gradLoss, &sigmoid](NodeCT* node) -> void { //pre-processing
                        summationGrad[node->getIndex()] = 0;
                        for(int p: node->getCNPs()){
                            summationGrad[node->getIndex()] += gradLoss[p];
                        }
                        summationGrad[node->getIndex()] = summationGrad[node->getIndex()] * sigmoid[node->getIndex()]; 
                    },
                    [&summationGrad](NodeCT* parent, NodeCT* child) -> void { //merge-processing
                        summationGrad[parent->getIndex()] += summationGrad[child->getIndex()];
                    },
                    [&summationGrad, &gradInput, &gradWeight,&gradBias, &dBias, &dWeight, &rows, &cols, &gradLoss ](NodeCT* node) -> void { //post-processing	
                        for(int p: node->getCNPs()){
                            gradInput[p] = summationGrad[node->getIndex()]; 
                            gradBias[0] += gradLoss[p] * dBias[node->getIndex()];
                            for (int j = 0; j < cols; j++)
                                gradWeight[j] += gradLoss[p] * dWeight[node->getIndex() + (rows * j)];
                            }		
                    }
            );
            
            
            delete[] summationGrad;
            py::array_t<float> gradWeight_np = py::array(py::buffer_info(
                    gradWeight,            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  cols }, 
                    { sizeof(float) }
            ));

            py::array_t<float> gradBias_np = py::array(py::buffer_info(
                    gradBias,            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  1 }, 
                    { sizeof(float) }
            ));

            py::array_t<float> gradInput_np = py::array(py::buffer_info(
                    gradInput,            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  tree->getNumRowsOfImage() * tree->getNumColsOfImage() }, 
                    { sizeof(float) }
            ));


            return py::make_tuple(gradWeight_np, gradBias_np, gradInput_np);
        }

};

#endif