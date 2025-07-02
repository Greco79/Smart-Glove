using UnityEngine;
using System.IO.Ports;

public class ArduinoControl : MonoBehaviour
{
    
    private string portName = "COM11"; // 串口号
    private int baudRate = 9600;      // 波特率
    private SerialPort serialPort;

    void Start()
    {
        OpenSerialPort();
    }

    void OnDestroy()
    {
        CloseSerialPort();
    }

    public void OpenSerialPort() // 将访问修饰符改为 public
    {
        if (serialPort == null || !serialPort.IsOpen)
        {
            serialPort = new SerialPort(portName, baudRate);
            serialPort.Open();
        }
    }

    public void CloseSerialPort()
    {
        if (serialPort != null && serialPort.IsOpen)
        {
            serialPort.Close();
            serialPort.Dispose();
            serialPort = null;
        }
    }

    // 向 Arduino 发送信号
    public void SendSignalToArduino(string signal)
    {
        OpenSerialPort(); // 打开串口

        if (serialPort != null && serialPort.IsOpen)
        {
            serialPort.WriteLine(signal);
            Debug.Log("Sent signal to Arduino: " + signal); // 在控制台中输出发送的信号
        }
        else
        {
            Debug.LogWarning("Serial port is not open or initialized."); // 输出警告信息
        }
    }
    
}
