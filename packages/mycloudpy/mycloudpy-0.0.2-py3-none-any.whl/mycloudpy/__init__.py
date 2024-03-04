import os,sys


def create_custom_page(repo_owner="", repo_title="", versions=[], description=""):
    version_strings=[]
    for version in versions:
        version_strings += ["""
<div id="{version}" onclick="load_readme('{version}', scroll_to_div=true)">
    <a href="git+https://github.com/{repo_owner}/{repo_title}@{version}#egg={repo_title}-version">{version}</a>
</div>
""".format(version=version)]

    return """
<!DOCTYPE html>
<html lang="en">
 <head>
  <!-- Required meta tags -->
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport"/>
  <!-- Skeleton CSS -->
  <link crossorigin="anonymous" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css" rel="stylesheet"/>
  <!-- Font -->
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&amp;display=swap" rel="stylesheet" type="text/css"/>
  <!-- JQuery -->
  <script src="https://code.jquery.com/jquery-latest.min.js">
  </script>
  <!-- Marked parser -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js">
  </script>
  <!-- Favicon -->
  <link href="https://gist.githubusercontent.com/franceme/c09af596e802e945d3032774e10e1047/raw/f693a2e2b65966494da082887bc4be2917f615e4/random_icon.svg" rel="icon"/>
  <!-- Custom Styles -->
  <link href="../static/package_styles.css" rel="stylesheet"/>
  <!-- Our JS -->
  <script src="../static/pypi_checker.js" type="text/javascript">
  </script>
  <script defer="" src="../static/package_page.js">
  </script>
  <title>
   Custom PyPi Page for {repo_title}
  </title>
 </head>
 <body>
  <div class="container">
   <section class="header">
    <button class="goback-button" onclick="redirectToIndex()">
     <svg height="50" width="50">
      <circle cx="25" cy="25" fill="#1EAEDB" r="20">
      </circle>
      <path d="M15 25l10-10v5h10v10h-10v5z" fill="white">
      </path>
     </svg>
    </button>
    {repo_title}
    <span>
    </span>
    <span class="version" id="latest-version">
     {latest}
    </span>
    <span hidden="" id="latest-main-version">
     {latest}
    </span>
   </section>
   <pre hidden="" id="installdanger">
      <button class="danger-button" disabled="">
        DANGER ! A higher version of <i>public-hello</i> already exists on PyPi
      </button>
    </pre>
   <pre id="installcmd">
      <code>{installcmd}</code>
    </pre>
   <hr/>
   <div class="row">
    <div class="three columns">
     <b>
      Project links
     </b>
     <button id="repoHomepage" onclick="openLinkInNewTab('https://github.com/{repo_owner}/{repo_title}')">
      Homepage
     </button>
     <p class="elem">
      <b>
       Author :
      </b>
      {repo_owner}
     </p>
     <section class="versions" id="versions">
      {version_strings}
     </section>
    </div>
    <div class="nine columns" id="description_pkg">
     <h6 class="text-header">
      {description}
     </h6>
     <p class="readme-block" id="markdown-container">
     </p>
    </div>
   </div>
  </div>
  <script>
   var url_readme_main = 'https://raw.githubusercontent.com/{repo_owner}/{repo_title}/main/README.md';
    
    $(document).ready(function () {{
      var this_vers = document.getElementById('latest-main-version').textContent.trim();
      document.getElementById(this_vers).classList.add('main');
      check_supply_chain_attack("{repo_title}", this_vers, warn_unsafe);
    
      if (window.location.hash != "") {{
        let version_hash = window.location.hash;
        version = version_hash.replace('#', '');
        load_readme(version, scroll_to_div=true);
        return;
      }}
      load_readme(this_vers);
    }});
  </script>
 </body>
</html>
""".strip().format(
        repo_owner=repo_owner,
        repo_title=repo_title,
        version_strings='\n'.join(version_strings),
        latest=max(versions),
        description=description,
        installcmd=create_import_cmd(
            repo_owner=repo_owner,
            repo_title=repo_title,
        )
    )

def html_string_prefix(repo_title=""):
    return """<a class="card" href="{repo_title}/">{repo_title}""".strip().format(repo_title=repo_title)

def create_latest_string(repo_title="", version="", description=""):
    return """
{prefix}<span></span><span class="version">{version}</span><br/><span class="description">{description}</span></a>
""".strip().format(
    prefix=html_string_prefix(repo_title=repo_title),
    version=version,
    description=description,
)

def create_import(repo_owner="", repo_title="", repo_version=None):
    string = """git+https://${{GITHUB_TOKEN}}@github.com/{repo_owner}/{repo_title}.git""".format(
        repo_owner=repo_owner,
        repo_title=repo_title,
    )
    if repo_version:
        string += "@{0}".format(repo_version)
    return string

def create_import_cmd(repo_owner="", repo_title="", repo_version=None):
    return "python3 -m pip install --upgrade " + str(create_import(
        repo_owner=repo_owner,
        repo_title=repo_title,
        repo_version=repo_version,
    ))