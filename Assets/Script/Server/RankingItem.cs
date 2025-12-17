using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class RankingItem : MonoBehaviour
{
    public TextMeshProUGUI rankText;
    public Image profileImage;
    public TextMeshProUGUI idText;
    public TextMeshProUGUI scoreText;
    public Sprite[] profileSprites;

    public void SetInfo(int rank, string id, int score, int profileIdx)
    {
        rankText.text = rank.ToString();
        idText.text = id;
        scoreText.text = score.ToString();

        // 프로필 이미지 배열 범위 확인 후 적용
        if (profileSprites != null && profileIdx >= 0 && profileIdx < profileSprites.Length)
        {
            profileImage.sprite = profileSprites[profileIdx];
        }
        else if (profileSprites != null && profileSprites.Length > 0)
        {
            // 범위를 벗어나면 기본 이미지(0번) 적용
            profileImage.sprite = profileSprites[0];
        }
    }
}
