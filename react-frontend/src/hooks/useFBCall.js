'use client';

import { useState, useCallback, useRef, useEffect, useMemo } from 'react';
import { Connection, Device } from "twilio-client";
import { getHackathonTwilioToken } from './api';
import { startHackathonCall } from './api';

// Keep track of existing device across all hook instances
const globalDeviceRef = {
  device: null,
  deviceId: null
};
            
export const useFBCall = ({ 
  device_id, 
  prompt, 
  responseHandlerUrl,
  twilioBackend = 'http://localhost:5000' 
}) => {
  const [activeConnection, setActiveConnection] = useState(null);
  const responseHandlerUrlRef = useRef(responseHandlerUrl);
  const isInitializedRef = useRef(false);

  const setupDevice = useCallback(async (token) => {
    // If we already have a device with this ID, don't create a new one
    if (globalDeviceRef.device && globalDeviceRef.deviceId === device_id) {
      console.log('Device already exists for this ID, reusing...');
      return globalDeviceRef.device;
    }

    console.log('Setting up new Twilio device...');
    try {
      // Cleanup any existing device first
      if (globalDeviceRef.device) {
        globalDeviceRef.device.destroy();
      }

      const newDevice = new Device(token, {
        codecPreferences: ['opus', 'pcmu'],
        debug: true
      });

      const eventHandlers = {
        ready: () => console.log('Twilio device is ready'),
        error: (error) => console.error('Twilio device error:', error),
        incoming: (conn) => {
          console.log('Incoming connection received');
          if (activeConnection) {
            console.log('Active connection exists, rejecting incoming');
            return;
          }
          console.log('Accepting incoming connection');
          conn.accept();
        },
        connect: (conn) => {
          console.log('Connection connected with details:', {
            status: conn?.status(),
            parameters: conn?.parameters,
            disconnect_cause: conn?.disconnect_cause,
            timestamp: new Date().toISOString()
          });
          setActiveConnection(conn);
        },
        disconnect: (conn) => {
          console.log('Connection disconnected with details:', {
            status: conn?.status(),
            parameters: conn?.parameters,
            disconnect_cause: conn?.disconnect_cause,
            timestamp: new Date().toISOString()
          });
          setActiveConnection(null);
        },
        cancel: () => {
          console.log('Connection cancelled');
          setActiveConnection(null);
        }
      };

      // Attach all event handlers
      Object.entries(eventHandlers).forEach(([event, handler]) => {
        newDevice.on(event, handler);
      });

      await new Promise((resolve) => {
        newDevice.on('ready', resolve);
      });

      // Store in global ref
      globalDeviceRef.device = newDevice;
      globalDeviceRef.deviceId = device_id;

      return newDevice;
    } catch (error) {
      console.error('Error setting up Twilio device:', error);
      throw error;
    }
  }, [device_id]);

  // Initialize device only once
  useEffect(() => {
    const initializeDevice = async () => {
      if (isInitializedRef.current) return;
      
      try {
        console.log('Initializing device with ID:', device_id);
        const token = await getHackathonTwilioToken(device_id, twilioBackend);
        await setupDevice(token);
        isInitializedRef.current = true;
      } catch (error) {
        console.error('Failed to initialize device:', error);
      }
    };

    if (device_id && !isInitializedRef.current) {
      initializeDevice();
    }

    // Cleanup function
    return () => {
      if (globalDeviceRef.deviceId === device_id) {
        console.log('Cleaning up device...');
        if (globalDeviceRef.device) {
          globalDeviceRef.device.destroy();
        }
        globalDeviceRef.device = null;
        globalDeviceRef.deviceId = null;
        isInitializedRef.current = false;
      }
    };
  }, []); // Empty dependency array ensures this only runs once

  const startCall = useCallback(async () => {
    console.log('startCall initiated');
    try {
      await startHackathonCall(
        device_id,
        prompt,
        responseHandlerUrlRef.current,
        twilioBackend
      );
      console.log('Call started successfully');
    } catch (error) {
      console.error('Failed to start call:', error);
      throw error;
    }
  }, [device_id, prompt, twilioBackend]);

  const endCall = useCallback(async () => {
    console.log('endCall initiated');
    try {
      if (activeConnection) {
        console.log('Active connection found, disconnecting...');
        activeConnection.disconnect();
        setActiveConnection(null);
        console.log('Call ended successfully');
      }
    } catch (error) {
      console.error('Failed to end call:', error);
      throw error;
    }
  }, [activeConnection]);

  return {
    isConnected: activeConnection !== null,
    startCall,
    endCall,
    activeConnection,
  };
}; 