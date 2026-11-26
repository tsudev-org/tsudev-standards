#!/usr/bin/env python3
"""Kiem thu noleak-guard.py bang du lieu GIA (khong co bi mat that). Chay: python3 scripts/agent-hooks/test-noleak-guard.py"""
import sys; sys.dont_write_bytecode = True  # khong sinh __pycache__
import json,subprocess,sys,os,tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(HERE,'noleak-guard.py')
S=tempfile.mkdtemp(); os.makedirs(S+'/proj')
open(S+'/proj/cf-token','w').write('fakeRAWvalue0123456789abcdefNOTREAL\n')
open(S+'/proj/.env','w').write('# c\nAPI_URL=https://x\nCF_API_TOKEN=notreal_notreal_notreal\nEMPTY=\n')
open(S+'/proj/.dev.vars','w').write('A=1\nrawlineNOTREAL123\n')
def run(tool,ti,ev="PreToolUse",resp=None):
    d={"hook_event_name":ev,"tool_name":tool,"tool_input":ti}
    if resp is not None: d["tool_response"]=resp
    o=subprocess.run(["python3",G],input=json.dumps(d),capture_output=True,text=True).stdout
    return "DENY" if '"deny"' in o else ("WARN" if "additionalContext" in o else "ok")
B=lambda c:run("Bash",{"command":c})
cases=[
 ("DENY",B(f"cut -d= -f1 {S}/proj/cf-token")),("DENY",B(f"cat {S}/proj/.env")),("DENY",B("printenv")),("DENY",B("env | sort")),
 ("DENY",B('echo "$CF_API_TOKEN"')),("DENY",B("gh auth token")),("DENY",B("gh auth status -t")),("DENY",B(f"grep TOKEN {S}/proj/.env")),
 ("DENY",B(f"X=$(cat {S}/proj/cf-token) && curl -H \"Authorization: Bearer $X\" x")),("DENY",B(f"source {S}/proj/cf-token")),
 ("DENY",B(f"head -1 < {S}/proj/cf-token")),("DENY",B("cat ~/.config/gh/hosts.yml")),("DENY",B("curl -v -H 'Authorization: Bearer $T' https://a")),
 ("DENY",B(f"python3 -c 'print(open(\"{S}/proj/.env\").read())' {S}/proj/.env")),("DENY",B(f"set -a; . {S}/proj/.dev.vars; set +a")),
 ("ok",B(f"set -a; . {S}/proj/.env; set +a; npm run deploy")),("ok",B("GH_TOKEN=$(gh auth token) gh api user -q .login")),
 ("ok",B(f"grep -q CF_API_TOKEN {S}/proj/.env && echo co")),("ok",B('[ -n "$CF_API_TOKEN" ] && echo "co, dai ${#CF_API_TOKEN}"')),
 ("ok",B(f"python3 {HERE}/noleak-inspect.py {S}/proj/cf-token")),("ok",B("cat > .env <<EOF\nA=1\nEOF")),("ok",B("cat package.json tokens/base.json")),
 ("ok",B("echo $HOME $PWD")),("ok",B("env NODE_ENV=production npm run build")),("ok",B("ls -la ~/.ssh && cat ~/.ssh/id_ed25519.pub")),
 ("ok",B("gh auth status")),("ok",B("cat .env.example")),("ok",B("compgen -v | grep -i token")),
 ("DENY",run("Read",{"file_path":f"{S}/proj/.env"})),("ok",run("Read",{"file_path":"/home/x/src/auth/token-service.ts"})),
 ("DENY",run("Grep",{"pattern":"TOKEN","glob":"**/.env*","output_mode":"content"})),("ok",run("Grep",{"pattern":"TOKEN","glob":"**/.env*"})),
 ("DENY",run("Write",{"file_path":"/r/README.md","content":"key ghp_"+"a"*36})),("ok",run("Write",{"file_path":"/r/.env","content":"GH=ghp_"+"a"*36})),
 ("ok",run("Write",{"file_path":"/r/a.ts","content":"const token = process.env.CF_API_TOKEN"})),
 ("DENY",B("git commit -m 'fix: key sk-ant-"+"x"*30+"'")),
 ("WARN",run("Bash",{"command":"x"},"PostToolUse",{"stdout":"value=ghp_"+"b"*36})),("ok",run("Bash",{"command":"x"},"PostToolUse",{"stdout":"all good"})),
 ("ok",B("python3 - <<'EOF'\nrule='cam printenv, env, set'\nEOF")),("DENY",B("bash <<EOF\nprintenv\nEOF")),
 ("DENY",B("git commit -F - <<'EOF'\nfix key sk-ant-"+"x"*30+"\nEOF")),("ok",B("cat > notes.md <<'EOF'\nkhong dung printenv\nEOF")),
]
bad=[(i,e,g) for i,(e,g) in enumerate(cases) if e!=g]; print(f"{len(cases)-len(bad)}/{len(cases)} dat"); print("SAI:",bad)
# noleak-inspect: --to-env (doi tep token tho -> KEY=VALUE, khong mat du lieu) + JSON + .b64
import hashlib
I=os.path.join(HERE,'noleak-inspect.py')
raw="fa'ke $HOME \"x\" `y` ;notreal"
open(S+'/pw','w').write(raw+'\n')
r1=subprocess.run(["python3",I,"--to-env","FAKE_PW",S+'/pw'],capture_output=True,text=True)
chk=subprocess.run(["bash","-c",'set -a; . "$1"; set +a; printf %s "$FAKE_PW" | sha256sum',"_",S+'/pw'],capture_output=True,text=True).stdout.split()[0]
open(S+'/j.json','w').write('{"access_token":"x","ab":"y"}')
r2=subprocess.run(["python3",I,S+'/j.json'],capture_output=True,text=True)
sys.path.insert(0,HERE); from noleaklib import is_secret_path
extra=[("ok" if r1.returncode==0 else "FAIL","ok"),(chk==hashlib.sha256(raw.encode()).hexdigest(),True),
       ("raw" in r1.stdout or raw in r1.stdout,False),(r2.returncode==0 and "- ab" in r2.stdout,True),
       (is_secret_path("ptsam.keystore.b64"),True),(is_secret_path("data.b64"),False)]
for i,(g,e) in enumerate(extra):
    if g!=e: bad.append(("inspect",i,e,g))
print(f"inspect: {sum(1 for g,e in extra if g==e)}/{len(extra)} dat")

# 12.2: tu chmod 600 khi ghi tep bi mat + SessionStart siet quyen / nhac phieu XK
R=tempfile.mkdtemp(); os.makedirs(R+'/logs/handover')
subprocess.run(['git','init','-q',R]); open(R+'/.gitignore','w').write('.env*\n')
open(R+'/.env','w').write('A=1\n'); os.chmod(R+'/.env',0o644)
open(R+'/logs/handover/20261126-XK1_t.md','w').write('# P\n- **Trạng thái**: MỞ\n')
pc=subprocess.run(['python3',os.path.join(HERE,'phase-context.py')],input=json.dumps({"cwd":R,"source":"startup"}),capture_output=True,text=True).stdout
open(R+'/.env.local','w').write('B=2\n'); os.chmod(R+'/.env.local',0o644)
subprocess.run(['python3',G],input=json.dumps({"hook_event_name":"PostToolUse","tool_name":"Bash","cwd":R,"tool_input":{"command":"printf B=2 > .env.local"},"tool_response":{"stdout":""}}),capture_output=True,text=True)
open(R+'/notes.md','w').write('x'); os.chmod(R+'/notes.md',0o644)
subprocess.run(['python3',G],input=json.dumps({"hook_event_name":"PostToolUse","tool_name":"Write","cwd":R,"tool_input":{"file_path":R+'/notes.md'},"tool_response":{}}),capture_output=True,text=True)
m=lambda f: oct(os.stat(R+'/'+f).st_mode&0o777)
x=[("XOAY KHOA" in pc,True),(m('.env'),'0o600'),(m('.env.local'),'0o600'),(m('notes.md'),'0o644')]
for i,(g,e) in enumerate(x):
    if g!=e: bad.append(("12.2",i,e,g))
print(f"12.2: {sum(1 for g,e in x if g==e)}/{len(x)} dat")

sys.exit(1 if bad else 0)
