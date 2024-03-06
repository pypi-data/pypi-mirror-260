import { Handle, Position } from 'reactflow';
import GetIcon from './GetIcon';
import * as faIcons from "react-icons/fa";
import { useReactFlow } from 'reactflow';
import { useState } from 'react';

function CustomNode({ data, type, id }) {
  const [name, setName] = useState(data?.label || type);
  const reactFlow = useReactFlow();
  

  const updateName = (e) => {
    setName(e.target.value.replace(/\n/g, ''));
    let new_nodes = []
    reactFlow.getNodes().map((node) => {
      if (node.id === id) {
        node.data = {
          ...node.data,
          label: e.target.value,
        };
      }
      new_nodes = new_nodes.concat(node)
    })
    reactFlow.setNodes(new_nodes)
  }

  return (
    <div className='text-xs'>
      {(data.port_selection == 'in' || data.port_selection == 'both') && (
        <Handle
          type="target"
          position={Position.Left}
        />
      )}
        <div className="flex flex-col items-center justify-center">
          <GetIcon icon={data?.icon || "FaCircle"} className="h-5 w-5 text-black-500" />
        </div>
        <textarea onChange={updateName} value={name} rows="1" class="line-clamp-1 w-5 resize-none border-none text-center block p-0 w-full text-xs text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" ></textarea>
      {(data.port_selection === 'out' || data.port_selection === 'both') && (
        <Handle
          type="source"
          position={Position.Right}
        />
      )}
    </div>
  );
}
export default CustomNode