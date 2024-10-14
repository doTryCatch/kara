import React from 'react'
import Main from './main'
export default function Home() {
  return (
    <div className='grid grid-rows-[20px_1fr_20px]   text-white items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]'>
      <div className='draggable '>
        {' '}
        {/* Draggable area */}
        Drag Me
      </div>
      <Main />
      <div> this will be setup of git in nvim</div>

      <div className='container bg-white text-white '>
        <h1>Hello, Electrion ui for jarvis!</h1>
        <p>This is a transparent window with click-through capability.</p>
      </div>
    </div>
  )
}
