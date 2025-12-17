using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ProfileSelector : MonoBehaviour
{
    public int SelectedIndex = 0; // 현재 선택된 인덱스 (기본값 0)
    public Image[] profileButtons; // UI의 버튼 이미지 배열

    public void SelectProfile(int index)
    {
        SelectedIndex = index;
        // 선택 시 시각적 효과 (예: 테두리 강조 등)를 여기에 추가할 수 있습니다.
        Debug.Log($"선택된 프로필 인덱스: {SelectedIndex}");
    }
}
