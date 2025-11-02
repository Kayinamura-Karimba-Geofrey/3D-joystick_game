using UnityEngine;
using System;
using System.Net.Sockets;
using System.IO;
using System.Threading;

public class BluetoothReceiver : MonoBehaviour
{
    public string host = "127.0.0.1";
    public int port = 5055;

    private TcpClient client;
    private StreamReader reader;
    private Thread netThread;

    private float pitch, roll;
    private object dataLock = new object();

    void Start()
    {
        netThread = new Thread(NetworkThread);
        netThread.IsBackground = true;
        netThread.Start();
    }

    void NetworkThread()
    {
        try
        {
            client = new TcpClient(host, port);
            reader = new StreamReader(client.GetStream());

            while (true)
            {
                string line = reader.ReadLine();
                if (line != null)
                {
                    string[] parts = line.Split(',');
                    if (parts.Length == 2)
                    {
                        float p, r;
                        if (float.TryParse(parts[0], out p) && float.TryParse(parts[1], out r))
                        {
                            lock (dataLock)
                            {
                                pitch = p;
                                roll = r;
                            }
                        }
                    }
                }
            }
        }
        catch (Exception e)
        {
            Debug.Log("Connection error: " + e.Message);
        }
    }

    void Update()
    {
        float p, r;
        lock (dataLock)
        {
            p = pitch;
            r = roll;
        }
        // Apply rotations
        transform.rotation = Quaternion.Euler(p, 0, -r);
    }

    void OnApplicationQuit()
    {
        if (netThread != null && netThread.IsAlive) netThread.Abort();
        if (reader != null) reader.Close();
        if (client != null) client.Close();
    }
}
