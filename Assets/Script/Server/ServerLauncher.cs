using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkConnector : MonoBehaviour
{
    [Header("Network Settings")]
    public string serverIP = "127.0.0.1";
    public int serverPort = 32452;

    void Awake()
    {
        // 1. 이미 초기화되었는지 확인 (혹시라도 씬을 다시 로드했을 때 방지)
        // NetworkManager 내부에 _isInitialized 체크가 있지만 여기서 한 번 더 해도 좋음

        // 2. 서버 매니저 초기화 및 접속 시도
        // (참고: NetworkManager.Initialize() 내부에서 Connect할 때 인자를 받도록 수정하거나,
        //  Network.Connect(serverIP, serverPort)를 호출하는 방식을 맞춰야 함)

        // 현재 NetworkManager 코드에는 IP/Port를 내부에서 "127.0.0.1"로 고정하고 있습니다.
        // 유연성을 위해 Initialize 호출 전이나 후에 IP를 설정하거나,
        // Initialize 함수가 IP, Port를 받도록 수정하는 것이 좋습니다.

        NetworkManager.Instance.Initialize();

        Debug.Log("네트워크 매니저 초기화 요청됨");
    }

    // ★★★ 가장 중요 ★★★
    // 이게 없으면 유니티 에디터에서 플레이 멈춤 눌러도
    // 백그라운드 스레드(NetworkReadThread)가 계속 살아서 에러를 뿜거나 유니티가 멈춥니다.
    void OnApplicationQuit()
    {
        NetworkManager.Instance.Stop();
        Debug.Log("네트워크 매니저 종료 및 스레드 정리됨");
    }
}
