using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SettingScript : MonoBehaviour
{
    public AudioSource audioSource; // 오디오 소스를 드래그로 연결
    public Slider volumeSlider; // Slider UI를 드래그로 연결

    private PlayerManager playerManager;
    private invenmanager inven;
    private ResourceManager resourceManager;

    [SerializeField] private TextMeshProUGUI volumeText;

    private const string VolumeKey = "Volume"; // PlayerPrefs 키값

    void Awake()
    {
        // 게임 시작 시 저장된 값 불러오기
        float savedVolume = PlayerPrefs.GetFloat(VolumeKey, 100f); // 저장된 볼륨 값, 없으면 기본값 100
        ApplyVolume(savedVolume);
    }

    void Start()
    {
        playerManager = PlayerManager.instance;
        inven = invenmanager.instance;
        resourceManager = ResourceManager.instance;
        // 슬라이더 초기값 설정
        if (volumeSlider != null)
        {
            volumeSlider.value = PlayerPrefs.GetFloat(VolumeKey, 100f); // 저장된 값을 슬라이더에 반영
            volumeSlider.onValueChanged.AddListener(OnVolumeChanged); // 슬라이더 값 변경 이벤트
        }
    }

    public void OnVolumeChanged(float sliderValue)
    {
        // 슬라이더 값 변경 시 볼륨 적용
        ApplyVolume(sliderValue);

        // PlayerPrefs에 볼륨 값 저장
        PlayerPrefs.SetFloat(VolumeKey, sliderValue);
        PlayerPrefs.Save();
    }

    private void ApplyVolume(float volume)
    {
        if (audioSource != null)
        {
            // Slider 값 (0~100)을 AudioSource.volume 값 (0~1)로 변환
            audioSource.volume = volume / 100f;
        }

        // 볼륨 텍스트 업데이트
        UpdateVolumeText(volume);
    }
    public void MasterID_For_Professor()
    {
        playerManager.gold = 10000000;
        playerManager.Playerlevel = 10;
        playerManager.AddResources_in_Player(500, 500, 500, 500);
        ResourceManager.instance.AddResource("탐험 허가증", 1000, 20);
    }
    private void UpdateVolumeText(float volume)
    {
        if (volumeText != null)
        {
            int volumeInt = Mathf.RoundToInt(volume); // 소수점 제거
            volumeText.text = $"{volumeInt}";
        }
    }

    public void QuitGame()
    {
        #if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
        #else
        Application.Quit();
        #endif

        Debug.Log("게임 종료");
    }
}
