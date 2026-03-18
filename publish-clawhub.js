const FormData = require('form-data');
const fetch = require('node-fetch').default;
const https = require('https');
const fs = require('fs');
const agent = new https.Agent({ rejectUnauthorized: false });

const form = new FormData();
form.append('package', fs.createReadStream('../qq-watermark-remover-v2.0.0.tar.gz'));
form.append('slug', 'qq-watermark-remover');
form.append('displayName', '豆包 AI 视频水印去除 (增强版 v2)');
form.append('version', '2.0.0');
form.append('changelog', 'v2 增强版发布');

console.log('尝试使用 FormData 上传 tar.gz 包到 ClawHub...');

fetch('https://clawhub.ai/api/cli/publish', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer clh_vKz-49HpVda2__-kWeYuvwcdmmMoURU6bgNGk01wTAQ',
    ...form.getHeaders()
  },
  body: form,
  agent
}).then(async r => {
  console.log('Status:', r.status);
  const text = await r.text();
  console.log('Response:', text);
  try {
    const json = JSON.parse(text);
    console.log('✅ Success!');
    console.log(JSON.stringify(json, null, 2));
  } catch(e) {
    console.log('Response text:', text);
  }
}).catch(e => console.error('Error:', e.message));
