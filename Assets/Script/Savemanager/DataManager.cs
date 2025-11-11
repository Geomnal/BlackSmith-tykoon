using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class DataManager : MonoBehaviour
{
    public PlayerManager playerManager;
    public ResourceManager resourcemanager;
    public invenmanager inven;
    public QuestSettingManager questSettingManager;


    [SerializeField] private List<hammerdata> hammerDatas; //해머 데이터를 불러오기 위해 데이터 매니저에 일단 해머데이터를 연결시켜주기로 함.
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject); // 씬이 바뀌어도 유지
        }
        else
        {
            Destroy(gameObject);
        }

        filePath = Path.Combine(Application.persistentDataPath, "playerData.json");
    }
    // Start is called before the first frame update
    private void Start()
    {
        playerManager = PlayerManager.instance;
        resourcemanager = ResourceManager.instance;
        questSettingManager = QuestSettingManager.instance;
        inven = invenmanager.instance;

    }

    // Update is called once per frame
    private void Update()
    {
        
    }
    public static DataManager instance;
    private string filePath;
    public hammerdata GetHammerDataByName(string hammerName)
    {
        return hammerDatas.Find(hammer => hammer.hammer_name == hammerName);
    }
    //설명하자면 복잡하다. 일단,iron과 wood도 이제 리소스 매니저에있는 걸 긁어온다..

    //자원은 해봤자 4개 이내이기에 이정도가 편할 거라 생각해 이렇게 구현했다.
    //플레이어 데이터는 플레이어 데이터를 긁어온다. 원래도 개별 변수이고 개별 변수를 가져와서 다시 개별 변수로 입히기에 큰 설명이 필요없다.
    //인벤 데이터.. 이게 문젠데 딕셔너리를 통으로 가져오는 건 json 파일이 불가능하다고 한다. 그래서 리스트를 만들어서 딕셔너리를 리스트 형태로 저장해놓고
    //다시 돌아왔을 때 ( 로드 버튼을 눌렀을 떄) 리스트를 다시 딕셔너리로 변환하는 과정을 거친다.
    public void SaveData()
    {
        if (ResourceManager.instance == null)
        {
            Debug.LogError("ResourceManager가 없습니다. 저장할 수 없습니다.");
        }


        // PlayerData에 저장할 정보 세팅
        PlayerData data = new PlayerData(PlayerManager.instance, GameObject.FindObjectOfType<invenmanager>());

        // JSON으로 변환 후 파일로 저장
        string json = JsonUtility.ToJson(data, true);
        try
        {
            File.WriteAllText(Application.persistentDataPath + "/playerData.json", json);
            Debug.Log("데이터가 저장되었습니다.");
        }
        catch (Exception e)
        {
            Debug.LogError("데이터 저장에 실패했습니다: " + e.Message);
        }
        Debug.Log("데이터가 저장되었습니다.");
        Debug.Log(Application.persistentDataPath);
    }
    public void LoadData()
    {
        string path = Application.persistentDataPath + "/playerData.json";
        if (File.Exists(path))
        {
            resourcemanager = FindObjectOfType<ResourceManager>();
            // JSON 파일에서 데이터 읽기
            string json = File.ReadAllText(path);
            PlayerData data = JsonUtility.FromJson<PlayerData>(json);
            // 불러온 데이터를 PlayerManager에 적용
            if (PlayerManager.instance != null)
            {
                PlayerManager.instance.brokenSword = data.brokenSword;
                PlayerManager.instance.reputation = data.reputation;
                PlayerManager.instance.gold = data.gold;
                PlayerManager.instance.Playerlevel = data.playerLevel;
                PlayerManager.instance.morality = data.morality;
                PlayerManager.instance.hammer_have = new List<int>(data.hammer_have);

                // hammerdataName 복원
                if (!string.IsNullOrEmpty(data.hammerdataName))
                {
                    hammerdata selectedHammer = GetHammerDataByName(data.hammerdataName);
                    if (selectedHammer != null)
                    {
                        PlayerManager.instance.CurrentHammerData = selectedHammer;
                    }
                    else
                    {
                        Debug.LogError($"Hammer '{data.hammerdataName}'를 찾을 수 없습니다.");
                    }
                }

            }
            else
            {
                Debug.Log("PlayerManager.instance가 없음.");
            }
            playerManager.UpdatebrokenswordUI();
            playerManager.UpdateUI();
            // ResourceManager를 통한 자원 설정
            if (ResourceManager.instance != null)
            {
                ResourceManager.instance.resources.Clear(); // 기존 데이터 초기화
                foreach (ResourceData resource in data.resourceDatas)
                {
                    ResourceManager.instance.resources.Add(resource.Resourcename, new Resource(resource.Resourcename, resource.price, resource.count));
                }
                ResourceManager.instance.FindUimanager(); // UI 갱신
            }
            else
            {
                Debug.LogWarning("ResourceManager.instance가 없음.");
            }
            ResourceManager.instance.FindUimanager(); // UI 매니저 연결
            Debug.Log("ResourceManager 데이터가 복원되었습니다.");

            playerManager.UpdateUI();
            questSettingManager.LevelUp_Quest_open();


            // invenmanager에 카운트 데이터 적용
            invenmanager inven = PlayerManager.instance.invenmanager;
            if (inven != null)
            {
                inven.itemCounts.Clear(); // 기존 데이터를 초기화하고 불러온 데이터를 추가
                foreach (ItemCountData item in data.itemCounts)
                {
                    inven.itemCounts.Add(item.itemName, item.count);
                }
                inven.UpdateUI(); // UI 업데이트
            }
            else
            {
                Debug.Log("Invenmanager null");
            }

            Debug.Log("데이터가 로드되었습니다.");
        }
        else
        {
            Debug.LogWarning("저장된 데이터 파일이 없습니다.");
        }

    }

    // 데이터 저장 함수
    public void SavePlayerData(PlayerManager player, invenmanager inven)
    {
        PlayerData data = new PlayerData(player, inven);
        string json = JsonUtility.ToJson(data, true);
        File.WriteAllText(filePath, json);
        Debug.Log("플레이어 데이터 저장.");
    }
    // HammerDatabase 내부 클래스
    [System.Serializable]
    public class HammerDatabase
    {
        public List<hammerdata> hammerDatas; // 모든 hammerdata를 저장하는 리스트

        public hammerdata GetHammerByName(string name)
        {
            return hammerDatas.Find(h => h.hammer_name == name);
        }
    }

    public HammerDatabase hammerDatabase;

}
