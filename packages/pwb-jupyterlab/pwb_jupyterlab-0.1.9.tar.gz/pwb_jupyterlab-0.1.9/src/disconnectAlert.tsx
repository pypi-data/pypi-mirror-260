/*
 * disconnectAlert.tsx
 *
 * Copyright (C) 2023 by Posit Software, PBC
 *
 */
import React, { useEffect, useState, useRef } from "react";
import { disconnectRetry, listen, Listener } from './disconnectMonitor';
import * as ReactDOM from 'react-dom';

export function WorkbenchDisconnectWidget(): JSX.Element {

  const [ message, setMessage ] = useState('');
  const [ visible, setVisible ] = useState(false);
  const [ onAccept, setOnAccept ] = useState<() => void>();
  const [ buttonFocus, setButtonFocus ] = useState(1);

  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let timestamp = 0;
    let timerId = -1;

    const updateMessage = () => {
      window.clearTimeout(timerId);
      const timeDiff = Date.now() - timestamp;
      const seconds = Math.floor(timeDiff / 1000);
      const minutes = Math.floor(seconds / 60);
      setMessage(`The underlying JupyterLab connection has been closed for <span aria-role="timer">${minutes}:${String(seconds % 60).padStart(2, '0')}</span>.<br>Attempting to reconnect...`);
      timerId = window.setTimeout(() => {
        updateMessage();
      }, 1000)
    }

    const listener: Listener = params => {
      if (typeof params.timestamp=== 'number') {
        timestamp = params.timestamp;
      }

      if (typeof params.onAccept === 'function') {
        setOnAccept(() => params.onAccept);
      }

      if (typeof params.dismiss === 'boolean') {
        setVisible(!params.dismiss);
        if(params.dismiss) {
          window.clearTimeout(timerId)
        } else {
          updateMessage();
        }
      }
    };

    const unlisten = listen(listener);

    return (() => {
      window.clearTimeout(timerId);
      unlisten();
    })
  }, [])

  const updateFocus = (direction = 0) => {
    if (!ref.current) { return; }


    const el = ref.current;
    const buttons = el.querySelectorAll('button');

    let currentFocus = buttonFocus;
    if (direction) {
      currentFocus = (buttons.length + currentFocus + Math.sign(direction)) % buttons.length;
    }

    buttons[currentFocus].focus()
    setButtonFocus(currentFocus);
  }

  useEffect(() => {
    if (!ref.current) { return; }

    const el = ref.current;

    el.style.display = '';

    const anim = el.animate([
      {
        opacity: visible ? 0 : 1 
      },
      {
        opacity: visible ? 1 : 0
      }
    ], 150)

    const onFinish = () => {
      el.style.display = visible ? '' : 'none'
      if (visible) {
        updateFocus();
      }
    }
  
    anim.addEventListener('finish', onFinish);

    return (() => {
      anim.removeEventListener('finish', onFinish)
    })
  }, [ visible ])

  const onKeyDown = (evt: React.KeyboardEvent<HTMLDivElement>) => {
    switch(evt.code) {
    case 'ArrowLeft':
    case 'ArrowRight':
    case 'Tab':
      evt.preventDefault();
      evt.stopPropagation();
      updateFocus(1);
    }
  }

  return (
    <div
      ref={ ref }
      id="workbench-disconnect-alert"
      className="jp-workbench-disconnect-alert jp-Dialog-content"
      style={ { display: 'none' } }
      tabIndex={ 0 }
      aria-role="alertdialog"
      aria-hidden={ !visible }
      aria-describedby="workbench-disconnect-alert-message"
      onKeyDown={ onKeyDown }
    >
      <div 
        id="workbench-disconnect-alert-message"
        style={ { gridArea: 'message' } }
        dangerouslySetInnerHTML={ { __html: message } }
      />
      <button 
        id="workbench-disconnect-alert-dismiss"
        style={ { gridArea: 'dismiss' } }
        className="jp-Dialog-button jp-mod-accept jp-mod-styled"
        onClick={ () => { onAccept && onAccept(); } }
        aria-label="Return to Workbench Home"
      >
        Workbench Home 
      </button>
      <button 
        id="workbench-disconnect-alert-retry"
        style={ { gridArea: 'retry' } }
        className="jp-Dialog-button jp-mod-reject jp-mod-styled"
        onClick={onAccept ? () => { disconnectRetry(onAccept); } : undefined}
        aria-label="Retry connection now"
      >
        Retry Now 
      </button>
    </div>
  )
}

export function setupDisconnectNotification() {
  const id = 'workbench-disconnect-layer'
  let host = document.getElementById(id)
  if (!host) { 
    host = document.createElement('div');
    host.id = id;
    host.style.cssText = `
      position: absolute;
      bottom: 26px;
      right: 34px;
      z-index: 1000;
    `;
    document.body.append(host);
  }
  ReactDOM.render(<WorkbenchDisconnectWidget/>, host);
}
