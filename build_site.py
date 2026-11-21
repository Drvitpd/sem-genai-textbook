import hashlib, json, re, qrcode, html
BASE = 'https://drvitpd.github.io/sem-genai-textbook/'
CODE = 'SEMGENAI2569'
norm = lambda s: re.sub(r'[\s\-]', '', s).upper()
H = hashlib.sha256(norm(CODE).encode()).hexdigest()
TITLE = 'SEM และ GenAI ในการวิจัยทางบัญชีและการสอบบัญชี'
SUB = 'กรณีศึกษาการนำ TSA for LCE มาใช้ในประเทศไทย'
rep = {n: json.load(open(f'/home/claude/book/rep{n:02d}.json')) for n in range(1, 14)}
GATE = '''<style>#gate{position:fixed;inset:0;background:#F2F7FB;z-index:99999;display:flex;align-items:center;justify-content:center;font-family:Sarabun,'Noto Sans Thai',sans-serif}
#gate .gb{background:#fff;border-top:4px solid #1F3864;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.08);padding:28px 26px;max-width:380px;width:88%;color:#222}
#gate h2{color:#1F3864;font-size:19px;margin:0 0 6px}#gate p{font-size:14px;margin:0 0 14px;line-height:1.6}
#gate .row{display:flex;gap:6px}#gate input[type=password],#gate input[type=text]{flex:1;font-size:16px;padding:9px 10px;border:1px solid #b8c4d4;border-radius:6px}
#gate button{font-family:inherit;font-size:15px;border:0;border-radius:6px;padding:9px 14px;cursor:pointer}#gate .sh{background:#E3E9F1;color:#1F3864}#gate .go{background:#1F3864;color:#fff;width:100%;margin-top:12px}
#gate label{font-size:13px;display:flex;gap:6px;align-items:center;margin-top:10px}#gate .err{color:#A93226;font-size:13px;min-height:18px;margin-top:8px}</style>
<div id="gate"><div class="gb"><h2>แอปประจำตำรา</h2><p>สำหรับผู้อ่านตำรา<br><b>''' + TITLE + '''</b><br>ใส่รหัสเข้าแอปที่พิมพ์ไว้ในตำรา</p>
<div class="row"><input id="gk" type="password" autocomplete="off" placeholder="รหัสเข้าแอป"><button class="sh" type="button" onclick="var i=document.getElementById('gk');i.type=i.type==='password'?'text':'password'">แสดง</button></div>
<label><input id="gr" type="checkbox"> จำรหัสในเครื่องนี้</label><button class="go" type="button" id="gg">เปิดแอป</button><div class="err" id="ge"></div></div></div>
<script>(function(){var H="''' + H + '''",K="semgenai_gate";
function ok(){var g=document.getElementById('gate');if(g)g.remove();}
try{if(localStorage.getItem(K)===H||sessionStorage.getItem(K)===H){ok();return;}}catch(e){}
async function chk(){var v=document.getElementById('gk').value.replace(/[\\s\\-]/g,'').toUpperCase();
var b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(v));var h=Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0')}).join('');
if(h===H){try{(document.getElementById('gr').checked?localStorage:sessionStorage).setItem(K,H)}catch(e){}ok();}else{document.getElementById('ge').textContent='รหัสไม่ถูกต้อง โปรดดูรหัสที่พิมพ์ไว้ในตำรา';}}
document.getElementById('gg').onclick=chk;document.getElementById('gk').addEventListener('keydown',function(e){if(e.key==='Enter')chk();});})();</script>'''
NAV = '<div style="font-family:Sarabun,sans-serif;font-size:13px;padding:8px 14px;background:#1F3864"><a href="index.html" style="color:#fff;text-decoration:none">← สารบัญแอปประจำตำรา</a></div>'
for n in range(1, 14):
    s = open(f'/home/claude/apps/ch{n}.html', encoding='utf8').read()
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + GATE + NAV, s, count=1)
    MOB = '<style>@media (max-width:640px){body *{min-width:0}table{display:block;overflow-x:auto;max-width:100%}th,td{white-space:normal}select,input,canvas,img,svg{max-width:100%}[class*=grid],.row,.seg,.stats{grid-template-columns:1fr!important;flex-wrap:wrap}pre{overflow-x:auto;white-space:pre-wrap}}</style>'
    s = s.replace('</head>', MOB + '</head>', 1)
    assert 'id="gate"' in s
    open(f'docs/ch{n:02d}.html', 'w', encoding='utf8').write(s)
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(f'{BASE}ch{n:02d}.html'); q.make(fit=True)
    q.make_image(fill_color='#1F3864', back_color='white').save(f'docs/qr/ch{n:02d}.png')
groups = [('ฐานคิด', [1, 2]), ('การวัด', [3, 4, 5, 6]), ('การทดสอบ', [7, 8, 9, 10]), ('เชิงคุณภาพ', [11, 12]), ('จริยธรรม', [13])]
items = ''
for g, chs in groups:
    items += f'<h3>{g}</h3>' + ''.join(f'<a class="c" href="ch{n:02d}.html"><b>บทที่ {n}</b><span>{html.escape(rep[n]["title"])}<i>{html.escape(rep[n]["en"])}</i></span></a>' for n in chs)
idx = f'''<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>แอปประจำตำรา · {TITLE}</title><link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>body{{margin:0;font-family:Sarabun,sans-serif;background:#F2F7FB;color:#222}}.w{{max-width:760px;margin:0 auto;padding:22px 16px 40px}}
.hd{{background:#fff;border-radius:10px;padding:18px 20px;border-top:4px solid #1F3864}}.hd img{{height:54px}}h1{{color:#1F3864;font-size:23px;margin:10px 0 2px;line-height:1.35}}.s{{color:#1F3864}}.en{{color:#666;font-style:italic;font-size:14px}}
.how{{background:#fff;border-left:4px solid #F39C12;border-radius:6px;padding:10px 14px;margin:14px 0;font-size:15px;line-height:1.65}}
h3{{color:#1F3864;margin:18px 0 6px;font-size:16px;border-bottom:1px solid #C9D3E0;padding-bottom:3px}}
a.c{{display:flex;gap:12px;background:#fff;border-radius:8px;padding:10px 14px;margin:6px 0;text-decoration:none;color:#222;box-shadow:0 1px 3px rgba(0,0,0,.05)}}a.c b{{color:#1F3864;white-space:nowrap}}a.c span{{display:flex;flex-direction:column}}a.c i{{color:#777;font-size:13px}}
.ft{{color:#777;font-size:12.5px;margin-top:26px;line-height:1.6}}</style></head><body>{GATE}<div class="w">
<div class="hd"><img src="logo-drvitpd.png" alt="Dr.VIT &amp; PD"><h1>{TITLE}</h1><div class="s">{SUB}</div><div class="en">SEM and Generative AI in Accounting and Auditing Research: The Case of TSA for LCE Adoption in Thailand</div><div style="margin-top:8px;font-weight:700">ดร.วิทยา อรุณศิริเพ็ชร</div></div>
<div class="how">แอปประจำบทใช้คู่กับตำรา แต่ละบทมีใบงานที่ผูกกับวัตถุประสงค์การเรียนรู้ (LO) และแบบทดสอบท้ายบทพร้อมคำอธิบาย ควรอ่านบทในตำราและทำแบบฝึกหัดก่อนเปิดแอป ตัวเลขทุกค่าในแอปเป็นข้อมูลสังเคราะห์เพื่อการสอน ห้ามนำข้อมูลผู้ตอบจริงใส่แอปหรือเครื่องมือ GenAI</div>
{items}<div class="ft">ข้อมูลเป็นปัจจุบัน ณ วันที่ 21 พฤศจิกายน 2569</div></div></body></html>'''
open('docs/index.html', 'w', encoding='utf8').write(idx)
open('docs/.nojekyll', 'w').write('')
open('README.md', 'w', encoding='utf8').write(f'# แอปประจำตำรา {TITLE}\n\n{SUB}\n\nผู้เขียน: ดร.วิทยา อรุณศิริเพ็ชร\n\nเว็บ: {BASE}\n\nแอปประจำบท 13 บท (docs/ch01.html–ch13.html) ใช้คู่กับตำรา ข้อมูลในแอปเป็นข้อมูลสังเคราะห์เพื่อการสอน\n')
print('ok', H[:12])
