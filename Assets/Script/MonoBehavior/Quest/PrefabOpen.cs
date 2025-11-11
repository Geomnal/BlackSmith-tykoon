using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public class PrefabOpen : MonoBehaviour
{
    [SerializeField] private GameObject questPrefab;
    private GameObject currentQuest;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void ShowQuest()
    {
        if (currentQuest == null) // Quest가 이미 화면에 나타나지 않았을 때만 생성
        {
            // Quest 1 Prefab을 main_Canvas의 자식으로 생성
            currentQuest = Instantiate(questPrefab, new Vector3(0, 0, 0), Quaternion.identity);

            // main_Canvas 찾기
            Transform canvasTransform = GameObject.Find("main_Canvas").transform;

            if (canvasTransform != null)
            {
                // 생성된 Prefab을 main_Canvas의 자식으로 설정
                currentQuest.transform.SetParent(canvasTransform, false);

                Debug.Log("Prefab 생성 완료!");
                Soundmanager.instance.PlayPapersound();
            }
            else
            {
                Debug.LogWarning("main_Canvas를 찾을 수 없습니다.");
            }
        }
    }
}
