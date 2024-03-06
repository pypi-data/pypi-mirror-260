import React from 'react';
// import "./sidebar.css"
const onDragStart = (event, nodeType) => {
  event.dataTransfer.setData('application/reactflow', nodeType);
  
  event.dataTransfer.effectAllowed = 'move';
};

const generateNode = (nodeType) => {
  let card_styling = "block max-w-sm m-1 p-1 bg-white border border-gray-200 rounded-sm shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
  return (
    <div key={nodeType} className={card_styling}
      onDragStart={(event) => onDragStart(event, nodeType,)} draggable
    >
      {nodeType}
    </div>)
}

const Sidebar = ({nodeTypes}) => {
  return (
    <aside className=' grow flex-row min-w-36 select-none '>
    {nodeTypes.map((key) => ( generateNode(key)))}
    </aside>
  );
};

export default Sidebar