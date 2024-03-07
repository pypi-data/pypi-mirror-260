
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

namespace py = pybind11;

#include "../include/ComputerDerivatives.hpp"
#include "../include/ComponentTree.hpp"
#include "../include/NodeCT.hpp"
#include "../include/AttributeComputedIncrementally.hpp"


ComputerDerivatives::ComputerDerivatives(){

}



py::tuple ComputerDerivatives::derivadaLoss_thetas(ComponentTree* tree, py::array_t<float> &attrs, std::vector<float> sigmoid, py::array_t<float> gradientOfLoss) {
    auto buf_attrs = attrs.request();
	float* attributes = (float *) buf_attrs.ptr;
    int rows = buf_attrs.shape[0];
    int cols = buf_attrs.shape[1];
    
    float *dWeight = new float[rows * cols];
    float *dBias = new float[rows];

    derivadaOutputThetas(tree, attributes, sigmoid, dWeight, dBias, rows, cols);

    auto buf_gradLoss = gradientOfLoss.request();
	float* gradLoss = (float *) buf_gradLoss.ptr;
    
    float *gradWeight = new float[cols];
    float *gradBias = new float[1];
    
    
    for (int pixel=0; pixel < tree->getNumRowsOfImage() * tree->getNumColsOfImage(); pixel++){
      int id = tree->getSC(pixel)->getIndex();
    
      if(pixel == 0){
        gradBias[0] = gradLoss[pixel] * dBias[id];
        for (int j = 0; j < cols; j++)
            gradWeight[j] = gradLoss[pixel] * dWeight[id + (rows * j)];
      }
      else{
        gradBias[0] += gradLoss[pixel] * dBias[id];
        for (int j = 0; j < cols; j++)
            gradWeight[j] += gradLoss[pixel] * dWeight[id + (rows * j)];
      }
    }

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
			[&summationGrad, &gradInput](NodeCT* node) -> void { //post-processing	
                for(int p: node->getCNPs()){
                    gradInput[p] = summationGrad[node->getIndex()]; 
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


void ComputerDerivatives::derivadaOutputThetas(ComponentTree* tree, float* attributes, std::vector<float> sigmoid, float *dWeight, float *dBias, int rows, int cols){
    

    for(NodeCT* node: tree->getListNodes()){
        int id = node->getIndex();
        dBias[id] = (sigmoid[id] * (1 - sigmoid[id])) * node->getResidue();

        //dWeight[id] = (sigmoid[id] * (1 - sigmoid[id])) * attributes[id] * h[id];
        for (int j = 0; j < cols; j++)
            dWeight[id + (rows * j)] = (sigmoid[id] * (1 - sigmoid[id])) * attributes[id + (rows * j)] * node->getResidue();

        if (id > 0) {
            int idParent = node->getParent()->getIndex();
            dBias[id] += dBias[idParent];

            //dWeight[id] += dWeight[idParent];
            for (int j = 0; j < cols; j++)
                dWeight[id + (rows * j)] += dWeight[idParent + rows * j];

            
        }
    }

}


py::tuple ComputerDerivatives::derivadaOutput_thetas(py::array_t<float> &attrs, std::vector<float> sigmoid, std::vector<int> h, std::vector<int> listIdsNodes, std::vector<int> listIdsParent){
    
    auto buf_attrs = attrs.request();
	float* attributes = (float *) buf_attrs.ptr;
    int rows = buf_attrs.shape[0];
    int cols = buf_attrs.shape[1];
    
    float *dWeight = new float[rows * cols];
    float *dBias = new float[listIdsNodes.size()];


    for (int i = 0; i < listIdsNodes.size(); i++) {
        int id = listIdsNodes[i];
        dBias[id] = (sigmoid[id] * (1 - sigmoid[id])) * h[id];

        //dWeight[id] = (sigmoid[id] * (1 - sigmoid[id])) * attributes[id] * h[id];
        for (int j = 0; j < cols; j++)
            dWeight[id + (rows * j)] = (sigmoid[id] * (1 - sigmoid[id])) * attributes[id + (rows * j)] * h[id];

        if (i > 0) {
            int idParent = listIdsParent[i];
            dBias[id] += dBias[idParent];

            //dWeight[id] += dWeight[idParent];
            for (int j = 0; j < cols; j++)
                dWeight[id + (rows * j)] += dWeight[idParent + (rows * j)];

            
        }
    }

    py::array_t<float> dWeight_np = py::array(py::buffer_info(
			dWeight,            
			sizeof(float),     
			py::format_descriptor<float>::value, 
			2,         
			{  rows, cols }, 
			{ sizeof(float), sizeof(float) * rows }
	));


    py::array_t<float> dBias_np = py::array(py::buffer_info(
			dBias,            
			sizeof(float),     
			py::format_descriptor<float>::value, 
			1,         
			{  listIdsNodes.size() }, 
			{ sizeof(float) }
	));

    return py::make_tuple(dWeight_np, dBias_np);
}