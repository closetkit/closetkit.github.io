// 사용: node render_frames.js <aspect v|h> <lang ko|ja> <out.mp4>   또는  --stills <aspect> <lang> f1,f2,...
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const stills = process.argv[2] === '--stills';
  const [aspect, lang, out] = stills ? process.argv.slice(3) : process.argv.slice(2);
  const V = aspect === 'v', W = V ? 1080 : 1920, H = V ? 1920 : 1080;
  const b = await chromium.launch({ args: ['--font-render-hinting=none'] });
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  pg.on('pageerror', e => console.error('pageerror', e.message));
  await pg.goto('file://' + path.join(__dirname, 'promo.html') + `?aspect=${aspect}&lang=${lang}`);
  await pg.evaluate(() => document.fonts.ready);
  if (stills) {
    require('fs').mkdirSync(path.join(__dirname, 'stills'), { recursive: true });
    for (const f of out.split(',').map(Number)) {
      await pg.evaluate(f => window.seek(f), f);
      await pg.screenshot({ path: path.join(__dirname, 'stills', `${aspect}-${lang}-${f}.png`) });
    }
    await b.close(); return;
  }
  const N = await pg.evaluate(() => window.N);
  // 무음 오디오 트랙 포함 (일부 앱·편집기 호환용)
  // 모션 블러: 프레임마다 반 프레임 간격 서브프레임 2장을 찍어 평균 (셔터 180°)
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '60', '-c:v', 'png', '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
    '-vf', "tmix=frames=2,select='mod(n,2)',setpts=N/(30*TB)",
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', '30',
    '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < N; f++) for (const sub of [0, 0.5]) {
    await pg.evaluate(f => window.seek(f), f + sub);
    const buf = await pg.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (sub) continue;
    if (f % 90 === 0) console.log(aspect, lang, f + '/' + N);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  console.log('saved', out);
})();
