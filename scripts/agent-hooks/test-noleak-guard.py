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
sys.exit(1 if bad else 0)
