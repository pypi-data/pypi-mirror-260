/*
 * disconnectMonitor.ts
 *
 * Copyright (C) 2023 by Posit Software, PBC
 *
 */
import { Dialog } from '@jupyterlab/apputils';
import { requestAPI } from './handler';
import { kHeartbeatEndpoint } from './constants';

let heartbeatId = -1

const retryIntervals = [ 2, 2, 2, 2, 5, 5, 10, 20, 30 ];
let retryCount = 0;
let retryTimer = -1;
let disconnectTimestamp = 0;

let existingDialog: Dialog<unknown> | undefined;

async function displayModal(onAccept: () => void) {

  // dialog already open, do not re-open
  // it is cleared when the user responds to input
  if (existingDialog) { return; }

  const acceptButton = Dialog.createButton({
    accept: true,
    label: 'Workbench Home'
  });

  const retryButton = Dialog.createButton({
    accept: false,
    label: 'Retry Now'
  });

  existingDialog = new Dialog ({
    body: 'The underlying JupyterLab connection has been closed.',
    title: 'Disconnected from Workbench',
    hasClose: false,
    buttons: [ acceptButton, retryButton ]
  });
  
  const result = await existingDialog.launch();
  if (result.button === acceptButton) {
    onAccept();
  } else if (result.button === retryButton) {
    disconnectRetry(onAccept);
  }
  existingDialog.close();
  existingDialog = undefined
}

export type Listener = (params: { timestamp?: number, dismiss?: boolean, onAccept?: () => void }) => void;
const listeners = new Set<Listener>();

export function listen(listener: Listener): () => void {
  const unlisten = () => {
    listeners.delete(listener);
  }
  listeners.add(listener);
  return unlisten;
}

function upsertNotification(onAccept: () => void) {
  for (const listener of listeners.values()) {
    listener({
      timestamp: disconnectTimestamp,
      dismiss: false,
      onAccept
    })
  }
}

function dismissNotification() {
  for (const listener of listeners) {
    listener({
      dismiss: true
    })
  }
}

export function disconnectRetry(returnHome: () => void) {
  // assume that we are dead in the water, start a series of delays to re-poll for connection
  // fire an event to the homepage to display an error
  const retryPoll = async (currentTry = retryCount) => {
    retryCount = currentTry;
    window.clearTimeout(retryTimer);
    try {
      const result = await requestAPI<{ result: boolean }>(kHeartbeatEndpoint);
      if (!result.result) { throw new Error('response was invalid'); }

      // if this succeeds then cancel retries and resume
      retryCount = 0;
      dismissNotification();
      heartbeat(returnHome)
    } catch (err) {
      // it's severe if we reach the end of retry intervals
      if (currentTry > 1) {
        if (retryCount < retryIntervals.length - 1) {
          // show / update notification
          upsertNotification(returnHome);
        } else {
          // show modal
          // this will just pause everything until the user does something about it,
          // since modals cannot be closed remotely
          dismissNotification();
          await displayModal(returnHome);
        }
      }
      retryTimer = window.setTimeout(
        () => { retryPoll(Math.min(currentTry + 1, retryIntervals.length - 1)); },
        retryIntervals[currentTry] * 1000
      );
    }
  };
  retryPoll();
}

export function heartbeat(returnHome: () => void) {
  window.clearTimeout(heartbeatId);
  heartbeatId = window.setTimeout(async () => {
    try {
      const result = await requestAPI<{ result: boolean }>(kHeartbeatEndpoint);
      if (!result.result) { throw new Error('response was invalid'); }
      heartbeat(returnHome);
    } catch (err) {
      disconnectTimestamp = Date.now();
      disconnectRetry(returnHome);
    }
  }, 30_000);
}

export function stopHeartbeat() {
  window.clearTimeout(heartbeatId);
}
