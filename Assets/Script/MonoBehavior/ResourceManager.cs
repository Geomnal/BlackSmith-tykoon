using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

// 앞으로 자원 등은 다 여기서 관리 할거임 다른 스크립트 만들지 말고 새로운 자원 추가하면 Mineral부터 뒤져보도록 하자
public class ResourceManager : MonoBehaviour
{
    public static ResourceManager instance;
    public Dictionary<string, Resource> resources = new Dictionary<string, Resource>();
    
    private UIManager uimanager;


    public PlayerManager playerManager;
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
        InitializeResources();
        uimanager = FindObjectOfType<UIManager>();
    }
    public void FindUimanager()
    {
        uimanager = FindObjectOfType<UIManager>();
    }
    private void Start()
    {
        

        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
        // "Player" 게임 오브젝트를 찾음
        playerManager = PlayerManager.instance;

        // null이면 디버그 처리
        if (playerManager == null)
        {
            Debug.LogError("PlayerManager를 찾을 수 없습니다.");
        }
    }
    private void Update()
    {
        resourcestext();
    }
    private void InitializeResources()
    {
        AddResource("철", 100, 0);
        AddResource("나무", 50, 0);
        AddResource("금", 100, 0);
        AddResource("텅스텐", 0, 0);
        AddResource("탐험 허가증", 1000, 0);
    }

    // 자원 추가 함수
    public void AddResource(string resourceName, int price, int amount)
    {
        if (resources.ContainsKey(resourceName))
        {
            resources[resourceName].AddResource_in_resourceclass(amount);
        }
        else
        {
            resources.Add(resourceName, new Resource(resourceName, price, amount));
        }
    }
    //json파일 불러오기용 setresource 함수이다.
    public void SetResource(string resourceName, int amount)
    {
        if (resources.ContainsKey(resourceName))
        {
            resources[resourceName].quantity = amount;
        }
        else
        {
            resources.Add(resourceName, new Resource(resourceName, 0, amount));
        }
    }
    //자원 소모 함수이다. 만약 플레이어가 해당 자원을 이거 이상으로 보유하지 못했을 시 false를 반환하여 플레이어의 자원 사용을 막아버린다.
    public bool UseResource(string resourceName, int amount)
    {
        if (resources.ContainsKey(resourceName))
        {
            return resources[resourceName].UseResource(amount);
        }
        Debug.LogWarning($"{resourceName} 자원이 없습니다.");
        return false;
    }
    // 자원 양 조회 함수
    public int GetResourceAmount(string resourceName)
    {
        if (resources.ContainsKey(resourceName))
        {
            return resources[resourceName].quantity;
            
        }
        else
        {
            Debug.Log("그런 자원 없습니다.");
            return 0;
        }
    }


    private void resourcestext()
    {
        if(uimanager != null)
        {
            uimanager.UpdateResourceUI();
        }
        
    }

    
}

public class Resource
{
    public string name;   // 자원의 이름
    public int price;     // 자원의 가격
    public int quantity;  // 플레이어가 보유한 자원의 양

    // 생성자: 자원의 이름, 가격, 보유량을 초기화
    public Resource(string name, int price, int quantity)
    {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    // 자원 추가 함수
    public void AddResource_in_resourceclass(int amount)
    {
        quantity += amount;
    }

    // 자원 소모 함수
    public bool UseResource(int amount)
    {
        if (quantity >= amount)
        {
            quantity -= amount;
            return true;
        }
        return false; // 자원이 부족할 경우 false 반환
    }
}