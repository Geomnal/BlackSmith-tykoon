using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[SerializeField]
public class PlayerData
{
    public List<ResourceData> resourceDatas;
    public int iron;
    public int wood;
    public int adventureTicket;
    public int brokenSword;
    public int reputation;
    public int gold;
    public int playerLevel;
    public int morality;

    public List<int> hammer_have; // hammer_have 리스트 추가
    public string hammerdataName; // hammerdata 이름 추가



    // invenmanager 관련 데이터 추가
    public List<ItemCountData> itemCounts;


    public PlayerData(PlayerManager player, invenmanager inven)
    {

        resourceDatas = new List<ResourceData>();
        if (ResourceManager.instance != null)
        {
            foreach (var resource in ResourceManager.instance.resources)
            {
                resourceDatas.Add(new ResourceData(resource.Value.name, resource.Value.price, resource.Value.quantity));
            }
        }

        brokenSword = player.brokenSword;
        reputation = player.reputation;
        gold = player.gold;
        playerLevel = player.Playerlevel;
        morality = player.morality;

        // hammer_have 리스트 저장
        hammer_have = new List<int>(player.hammer_have);
        // 현재 장착된 hammerdata 이름 저장
        hammerdataName = (player.hammerdata != null && !string.IsNullOrEmpty(player.hammerdata.hammer_name))
            ? player.hammerdata.hammer_name
            : "돌 망치";

        itemCounts = new List<ItemCountData>();
        foreach (KeyValuePair<string, int> item in inven.itemCounts)
        {
            itemCounts.Add(new ItemCountData(item.Key, item.Value));
        }

    }


}
//json 파일이 딕셔너리를 지원하지 않으므로. 새롭게 저장하기 위해 리스트를 사용했다. .. 하아...
[System.Serializable]
public class ItemCountData
{
    public string itemName;  // 아이템 이름
    public int count;        // 아이템 개수

    public ItemCountData(string itemName, int count)
    {
        this.itemName = itemName;
        this.count = count;
    }
}

[System.Serializable]
public class ResourceData
{
    public string Resourcename; // 자원의 이름
    public int price;           // 자원의 가격
    public int count;           // 자원의 개수

    public ResourceData(string resourcename, int price, int count)
    {
        Resourcename = resourcename;
        this.price = price;
        this.count = count;
    }
}