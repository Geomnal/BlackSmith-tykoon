using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Soundmanager : MonoBehaviour
{
    public static Soundmanager instance { get; set; }
    [SerializeField]
    private AudioSource hammerSource;
    [SerializeField]
    private AudioSource GoldSource;
    [SerializeField]
    private AudioSource PaperSource;
    [SerializeField]
    private AudioSource hitstoneSource;
    [SerializeField]
    private AudioSource breakstoneSource;
    [SerializeField]
    private AudioSource hitwoodSource;
    [SerializeField]
    private AudioSource breakwoodSource;
    [SerializeField]
    private AudioClip hammersound;
    [SerializeField]
    private AudioClip hitstonesound;
    [SerializeField]
    private AudioClip breakstonesound;
    [SerializeField]
    private AudioClip Goldsound;
    [SerializeField]
    private AudioClip Papersound;
    [SerializeField]
    private AudioClip hitwoodsound;
    [SerializeField]
    private AudioClip breakwoodsound;
    // Start is called before the first frame update
    private void Awake()
    {
        if(instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(gameObject);
        }

    }
    private void Start()
    {
        
    }
    // Update is called once per frame
    private void Update()
    {

    }
    public void PlayHammersound()
    {
        hammerSource.clip = hammersound;
        hammerSource.Play();
    }
    public void PlayPapersound()
    {
        PaperSource.clip = Papersound;
        PaperSource.Play();
    }
    public void PlayGoldsound()
    {
        GoldSource.clip = Goldsound;
        GoldSource.Play();
    }
    public void Playhitstonesound()
    {
        hitstoneSource.clip = hitstonesound;
        hitstoneSource.Play();
    }
    public void Playbreakstonesound()
    {
        breakstoneSource.clip = breakstonesound;
        breakstoneSource.Play();
    }
    public void Playhitwoodsound()
    {
        hitwoodSource.clip = hitwoodsound;
        hitwoodSource.Play();
    }
    public void Playbreakwoodsound()
    {
        breakwoodSource.clip = breakwoodsound;
        breakwoodSource.Play();
    }
}
