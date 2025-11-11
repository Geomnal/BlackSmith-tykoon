using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using UnityEngine;

public class explansupport : MonoBehaviour
{

    [SerializeField]private List<GameObject> Gameexp;  // 이미지 리스트
    [SerializeField] private int nowexp = 0;  // 현재 활성화된 이미지의 인덱스
    [SerializeField] private GameObject nextbutton;
    [SerializeField] private GameObject backbutton;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
    }

    // 클릭된 버튼에 해당하는 이미지를 활성화하고 나머지는 비활성화
    private void imageController(int index)
    {
        // 리스트의 모든 이미지를 비활성화
        foreach (GameObject gameObject in Gameexp)
        {
            gameObject.SetActive(false);
        }

        // 선택된 인덱스의 이미지만 활성화
        if (index >= 0 && index < Gameexp.Count)  // 유효한 인덱스인지 확인
        {
            Gameexp[index].gameObject.SetActive(true);
        }

    }
    public void nextbuttonclick()
    {
        nowexp = nowexp + 1;
        imageController(nowexp);
        
        if(nowexp >= 1)
        {
            backbutton.SetActive(true);
        }
        if(nowexp == 4) 
        {
            nextbutton.SetActive(false);
        }
    }
    public void backbuttonclick()
    {
        nowexp = nowexp - 1;
        imageController(nowexp);
        
        if (nowexp == 0)
        {
            backbutton.SetActive(false);
        }
        if (nowexp <= 3)
        {
            nextbutton.SetActive(true);
        }
    }
}
