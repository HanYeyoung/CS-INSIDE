import React from 'react'
import MessageHeader from './MessageHeader'

const MainPanel = () => {
  return (
    <div>
        <MessageHeader />

        <div
            style={{
                width: '100%',
                height: '450',
                border: '0.2rem solid #ecec',
                borderRadius: '4px',
                marginBottom: '1rem',
                overflowY: 'auto'
            }}
            >
        </div>
    </div>
  )
}

export default MainPanel;