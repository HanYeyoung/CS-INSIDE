import React from 'react'
import UserPanel from './UserPanel';
import Favorite from './Favorite';
import ChatRooms from './ChatRooms';
import DirectMessage from './DirectMessage';

function SidePanel() {
  return (
    <div style={{
        backgroundColor: "#7B83EB",
        padding: '2rem',
        minHeight: '100vh',
        color: 'white',
        minWidth: '275px'
    }}>
        <UserPanel />

        <Favorite />

        <ChatRooms />
        
        <DirectMessage />

        <button
        onClick={() => navigate('/Chatbot')} // Adjust route to your chatbot path
        style={{
          backgroundColor: "yellow",
          color: "black",
          border: "none",
          borderRadius: "50%",
          width: "60px",
          height: "60px",
          fontSize: "24px",
          fontWeight: "bold",
          cursor: "pointer",
          position: "absolute", // Positioning relative to the side panel
          bottom: "20px",
          left: "150px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        }}
        >
        💬
      </button>
    </div>
  )
}

export default SidePanel;