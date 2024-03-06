import { Streamlit } from "streamlit-component-lib"
import { useRenderData } from "streamlit-component-lib-react-hooks"
import React, { useState, useRef, useCallback, useEffect, useMemo } from "react"
import ReactFlow, {
  useNodesState, useEdgesState, addEdge, ReactFlowProvider, MiniMap,
} from 'reactflow';
import 'reactflow/dist/style.css';
import Sidebar from './Sidebar';
import CustomNode from "./Node";

function App() {
  console.log('hi')
  const reactFlowWrapper = useRef(null);
  // const { setViewport } = useReactFlow();

  const renderData = useRenderData()

  const [isFocused, setIsFocused] = useState(false)
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  useEffect(() => {
    const model = renderData.args["model"] || { nodes: [], edges: [] }
    if (model) {
      console.log(model)
      setNodes(model.nodes || []);
      setEdges(model.edges || []);
      // setViewport({ x, y, zoom });
    }
  }, [])

  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const initialNodeTypesDef = {
    'Test 1': {"color":"rgb(255,0, 192)", "port_selection" : 'out'},
    'Test 2': {"color":"rgb(255,0, 192)", "port_selection" : 'in'},
    'Test 3': {"color":"rgb(255,0, 192)", "port_selection" : 'both'},
    }
  const nodeTypesDef = renderData.args?.nodesTypes || initialNodeTypesDef
  // const nodeTypesDef = renderData.args?.nodesTypes
  let tempNodeTypes = {}
  Object.keys(nodeTypesDef).map((nodeDef) => {
    tempNodeTypes[nodeDef] = CustomNode
  })

  const nodeTypes = useMemo(() => (tempNodeTypes), []); 

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  useEffect(() => {
    if (reactFlowInstance){
      const flow = reactFlowInstance.toObject();
      Streamlit.setComponentValue(flow)
      console.log(flow)
    }
    Streamlit.setFrameHeight()
  }, [nodes, edges])

  const theme = renderData.theme
  const style = {}
  if (theme) {
    // Use the theme object to style our button border. Alternatively, the
    // theme style is defined in CSS vars.
    const borderStyling = `1px solid ${isFocused ? theme.primaryColor : "gray"}`
    style.border = borderStyling
    style.outline = borderStyling
  }

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);
  
  

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');

      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      
      setNodes((nds) => {

        let node_id = (nds?.length || 0 )
        const newNode = {
            id: `${node_id}`,
            type,
            position,
            data: { 
              label: `${type} node ${node_id}`,
              icon: 'FaBox',
              ...nodeTypesDef[type]
            },
          };
        return nds.concat(newNode)
      });
    },
    [reactFlowInstance],
  );
  return (

    <div className="flex h-[800px] grow w-screen ">
      <div className="h-[800px]" hidden></div> {/* add tailwind style that we want to include in final bundle */}
      <ReactFlowProvider>
        <div
          className="grow flex w-screen !h-100 flex-row flex-grow-1 bg-gray-50 border-l-rose-600"
        >
          {/* w-[100%] bg-gray-50 border-l-rose-600 reactflow-wrapper !h-100" */}
          <Sidebar nodeTypes = {Object.keys(nodeTypesDef)} />
          <div className="reactflow-wrapper !h-[100%] w-screen " ref={reactFlowWrapper}>
            <ReactFlow
              nodeTypes={nodeTypes} 
              nodes={nodes}
              onNodesChange={onNodesChange}
              edges={edges}
              onEdgesChange={onEdgesChange}
              fitView
              onConnect={onConnect}
              onDrop={onDrop}
              onDragOver={onDragOver}
              onInit={(reactFlowInstance) => setReactFlowInstance(reactFlowInstance)}
              className="bg-gray-50"
            >
              <MiniMap />
            </ReactFlow>
          </div>

        </div>

        <div className="flex w-[20%]">

        </div>
      </ReactFlowProvider>
    </div>
  );
}

export default App
