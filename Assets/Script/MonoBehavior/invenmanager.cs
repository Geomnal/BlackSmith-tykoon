using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class invenmanager : MonoBehaviour
{
    public static invenmanager instance;
    public PlayerManager PlayerManager;
    private UIManager uimanager;


    // Start is called before the first frame update
    //철검 제작 횟수 증가 및 텍스트 업데이트 함수까지 호출해주는 함수

    public Dictionary<string, int> itemCounts = new Dictionary<string, int>();
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject); // 씬이 바뀌어도 유지
        }
        else
        {
            Destroy(gameObject); // 이미 인스턴스가 존재하면 새로 생긴 객체를 파괴

        }
        DictionaryUpdate();
        uimanager = UIManager.instance;
    }
    public void FindUimanager()
    {
        uimanager = UIManager.instance;
    }
    private void Start()
    {
    
        if (uimanager != null)
        {
            uimanager.UpdatePlayerUI();
        }
        UpdateUI();
    }
    // Update is called once per frame
    private void Update()
    {
        FindUimanager();
    }

    public void IncreaseItemCount(Itemdata itemdata)
    {
        if (itemCounts.ContainsKey(itemdata.itemname))
        {
            itemCounts[itemdata.itemname] = itemCounts[itemdata.itemname] + 1;  
            UpdateUI();
        }
        else
        {
            Debug.LogError("잘못된 아이템 이름: " + itemdata.itemname);
        }
    }
    public void IncreaseItemCount_in_stringint(string itemName, int count)
    {
        if (itemCounts.ContainsKey(itemName))
        {
            itemCounts[itemName] += count;
            UpdateUI();
        }
        else
        {
            Debug.LogError("잘못된 아이템 이름: " + itemName);
        }
    }
    public void UpdateUI()
    {
        if (uimanager != null)
        {
            uimanager.UpdateInventoryUI();
        }
        else
        {
            uimanager = FindObjectOfType<UIManager>();
        }
    }

    public void DictionaryUpdate()
    {
        itemCounts["철 검"] = 0;
        itemCounts["나무 검"] = 0;
        itemCounts["철 갑옷"] = 0;
        itemCounts["철 괭이"] = 0;
        itemCounts["철 방패"] = 0;
        itemCounts["철 창"] = 0;
        itemCounts["철 검 묶음"] = 0;
        itemCounts["은 목걸이"] = 0;
        itemCounts["강철 검"] = 0;
        itemCounts["금 목걸이"] = 0;
        itemCounts["금 갑옷"] = 0;
        itemCounts["마검 - 사라트"] = 0;
        itemCounts["마검 - 삼위일체"] = 0;
        itemCounts["마검 - 알 반살"] = 0;
        itemCounts["마검 - 본다르"] = 0;
    }
    public void UpdateAllUIText()
    {
        foreach (KeyValuePair<string, int> item in itemCounts)
        {
            UpdateUI();
        }
    }
    //불러오기 후 변수와 딕셔너리 동기화
    public void LoadDataAndSync()
    {
        UpdateUI();
    }



}
