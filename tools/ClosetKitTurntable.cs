// Closet Kit — 360° 촬영 (Unity 2022.3 / VRChat SDK 프로젝트)
// 넣는 곳: Assets/Editor/ClosetKitTurntable.cs   →   메뉴 Tools > Closet Kit > 360° 촬영
//
// 카메라가 아바타 주위를 한 바퀴 돌며 각도별 PNG 를 찍습니다 (아바타는 움직이지 않아 PhysBone 이 흔들리지 않음).
// 결과: <프로젝트 폴더>/ClosetKitTurntable/<아바타 id>/<옷 id>/00.png … 35.png
// 프레임 번호가 커질수록 아바타 정면이 화면 오른쪽으로 돌아갑니다 (사이트 뷰어와 같은 방향).
//
// 업로드 결과와 똑같이 찍으려면: Play 모드(NDMF/Modular Avatar 의 Apply on Play)에서
// Gesture Manager 등으로 옷을 바꾼 뒤, Hierarchy 의 Play 중인 아바타를 넣고 촬영하세요.
#if UNITY_EDITOR
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEngine;

public class ClosetKitTurntable : EditorWindow
{
    GameObject avatar;
    string avatarId = "";
    string outfitId = "outfit1";
    int frames = 36;
    int width = 900, height = 1200;
    float frameHeight = 0f;        // 화면 세로에 담을 높이(m). 옷마다 같은 값을 써야 옷을 바꿔도 크기가 안 튐
    float fov = 18f;               // 좁을수록 원근 왜곡이 적음
    float yOffset = 0f;            // 카메라 높이 미세 조정(m)
    bool transparent = true;
    Color background = new Color(0.94f, 0.93f, 0.97f, 1f);
    bool keyLight = true;
    float lightIntensity = 0.8f;
    Texture2D preview;

    const int Layer = 31;          // 촬영하는 동안만 아바타를 이 레이어로 옮겨 다른 물체가 안 찍히게 함

    [MenuItem("Tools/Closet Kit/360° 촬영")]
    static void Open() { GetWindow<ClosetKitTurntable>("Closet Kit 360°").minSize = new Vector2(340, 520); }

    void OnGUI()
    {
        EditorGUILayout.LabelField("아바타", EditorStyles.boldLabel);
        var a = (GameObject)EditorGUILayout.ObjectField("아바타 루트", avatar, typeof(GameObject), true);
        if (a != avatar) { avatar = a; if (avatar && string.IsNullOrEmpty(avatarId)) avatarId = Slug(avatar.name); }
        avatarId = EditorGUILayout.TextField("아바타 id (영문)", avatarId);
        outfitId = EditorGUILayout.TextField("옷 id (영문)", outfitId);
        EditorGUILayout.HelpBox("옷마다 옷 id 를 바꿔 가며 한 번씩 촬영하세요. 예) katana, devicute", MessageType.None);

        EditorGUILayout.Space();
        EditorGUILayout.LabelField("촬영", EditorStyles.boldLabel);
        frames = EditorGUILayout.IntSlider("각도 수", frames, 12, 72);
        width = EditorGUILayout.IntField("가로(px)", width);
        height = EditorGUILayout.IntField("세로(px)", height);
        using (new EditorGUILayout.HorizontalScope())
        {
            frameHeight = EditorGUILayout.FloatField("담을 높이(m)", frameHeight);
            if (GUILayout.Button("자동", GUILayout.Width(50)) && avatar) frameHeight = AutoHeight();
        }
        EditorGUILayout.HelpBox("날개·모자처럼 가장 큰 옷을 입힌 상태에서 '자동'을 한 번 누르고, 그 값을 모든 옷에 그대로 쓰세요.", MessageType.Info);
        fov = EditorGUILayout.Slider("화각", fov, 10f, 40f);
        yOffset = EditorGUILayout.Slider("카메라 높이 조정(m)", yOffset, -0.5f, 0.5f);
        transparent = EditorGUILayout.Toggle("투명 배경", transparent);
        if (!transparent) background = EditorGUILayout.ColorField("배경색", background);
        keyLight = EditorGUILayout.Toggle("카메라 조명 추가", keyLight);
        if (keyLight) lightIntensity = EditorGUILayout.Slider("조명 세기", lightIntensity, 0f, 2f);

        EditorGUILayout.Space();
        using (new EditorGUI.DisabledScope(!avatar))
        {
            if (GUILayout.Button("미리보기 (정면)")) { if (frameHeight <= 0) frameHeight = AutoHeight(); preview = Shoot(0, 1, null); }
            if (GUILayout.Button($"촬영 — {frames}장", GUILayout.Height(32))) Capture();
        }
        if (preview)
        {
            var r = GUILayoutUtility.GetAspectRect((float)preview.width / preview.height, GUILayout.MaxHeight(320));
            EditorGUI.DrawTextureTransparent(r, preview, ScaleMode.ScaleToFit);
        }
    }

    static string Slug(string s)
    {
        s = Regex.Replace(s.Replace("(Clone)", ""), "[^A-Za-z0-9_-]+", "-").Trim('-').ToLowerInvariant();
        return string.IsNullOrEmpty(s) ? "avatar" : s;
    }

    float AutoHeight()
    {
        float top = avatar.transform.position.y;
        foreach (var r in avatar.GetComponentsInChildren<Renderer>())
            if (r.enabled && r.gameObject.activeInHierarchy && !(r is ParticleSystemRenderer)) top = Mathf.Max(top, r.bounds.max.y);
        return Mathf.Round((top - avatar.transform.position.y) * 1.06f * 100f) / 100f;
    }

    void Capture()
    {
        if (frameHeight <= 0) frameHeight = AutoHeight();
        string dir = Path.Combine(Path.GetDirectoryName(Application.dataPath), "ClosetKitTurntable", Slug(avatarId), Slug(outfitId));
        Directory.CreateDirectory(dir);
        foreach (var f in Directory.GetFiles(dir, "*.png")) File.Delete(f);
        try
        {
            for (int i = 0; i < frames; i++)
            {
                if (EditorUtility.DisplayCancelableProgressBar("Closet Kit 360°", $"{Slug(outfitId)} — {i + 1}/{frames}", (float)i / frames)) break;
                var tex = Shoot(i, frames, Path.Combine(dir, i.ToString("00") + ".png"));
                if (i == 0) preview = tex; else DestroyImmediate(tex);
            }
            File.WriteAllText(Path.Combine(dir, "manifest.json"),
                $"{{\"frames\":{frames},\"width\":{width},\"height\":{height},\"frameHeight\":{frameHeight},\"fov\":{fov}}}");
        }
        finally { EditorUtility.ClearProgressBar(); }
        EditorUtility.RevealInFinder(dir);
    }

    // index 번째 각도를 찍어서 (path 가 있으면) PNG 로 저장하고 Texture2D 를 돌려줌
    Texture2D Shoot(int index, int count, string path)
    {
        var root = avatar.transform;
        var center = root.position + Vector3.up * (frameHeight * 0.5f + yOffset);
        float dist = frameHeight * 0.5f / Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad);
        var dirFront = Vector3.ProjectOnPlane(root.forward, Vector3.up).normalized;
        if (dirFront.sqrMagnitude < 0.5f) dirFront = Vector3.forward;
        // 카메라가 위에서 볼 때 시계 방향(아바타의 오른쪽)으로 돌면 화면에서는 정면이 오른쪽으로 돌아감
        var camDir = Quaternion.AngleAxis(360f * index / count, Vector3.up) * dirFront;

        var go = new GameObject("ClosetKit_TurntableCam") { hideFlags = HideFlags.HideAndDontSave };
        var cam = go.AddComponent<Camera>();
        cam.enabled = false;
        cam.fieldOfView = fov; cam.nearClipPlane = 0.05f; cam.farClipPlane = dist * 4f;
        cam.clearFlags = CameraClearFlags.SolidColor;
        cam.backgroundColor = transparent ? new Color(0, 0, 0, 0) : background;
        cam.cullingMask = 1 << Layer;
        cam.allowHDR = false; cam.allowMSAA = true;
        go.transform.position = center + camDir * dist;
        go.transform.LookAt(center, Vector3.up);

        Light light = null;
        if (keyLight)
        {
            var lg = new GameObject("ClosetKit_KeyLight") { hideFlags = HideFlags.HideAndDontSave };
            lg.transform.SetParent(go.transform, false);
            lg.transform.localRotation = Quaternion.Euler(25f, 30f, 0f);    // 카메라 왼쪽 위에서 오른쪽 아래로 비추는 조명
            light = lg.AddComponent<Light>();
            light.type = LightType.Directional; light.intensity = lightIntensity; light.shadows = LightShadows.Soft;
        }

        var layers = new List<(GameObject, int)>();
        foreach (var t in avatar.GetComponentsInChildren<Transform>(true)) { layers.Add((t.gameObject, t.gameObject.layer)); t.gameObject.layer = Layer; }
        var msaa = new RenderTexture(width, height, 24, RenderTextureFormat.ARGB32) { antiAliasing = 8 };
        var rt = new RenderTexture(width, height, 0, RenderTextureFormat.ARGB32);
        var prev = RenderTexture.active;
        var tex = new Texture2D(width, height, TextureFormat.RGBA32, false);
        try
        {
            cam.targetTexture = msaa;
            cam.Render();
            Graphics.Blit(msaa, rt);                  // MSAA 해제
            RenderTexture.active = rt;
            tex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
            tex.Apply();
            if (path != null) File.WriteAllBytes(path, tex.EncodeToPNG());
        }
        finally
        {
            RenderTexture.active = prev;
            cam.targetTexture = null;
            foreach (var p in layers) if (p.Item1) p.Item1.layer = p.Item2;
            msaa.Release(); rt.Release(); DestroyImmediate(msaa); DestroyImmediate(rt);
            DestroyImmediate(go);                     // 카메라·조명 함께 삭제
        }
        return tex;
    }
}
#endif
