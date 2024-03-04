![Subdora Logo](https://raw.githubusercontent.com/Lakshit-Karsoliya/Subdora/main/assets/subdora.png "Subdora")
 

[Github](https://github.com/Lakshit-Karsoliya/Subdora)

<h1>Subdora 0.0.1</h1>

<p>This is initial release of subdora. Subdora is an obfuscation tool which makes source code very hard to interprate</p>

<h2>How to use</h2>
<h3>Core functionality</h3>

<p>obfuscating main.py file </p>


<code>import Subdora</code></br>
<code>Subdora.subdora_encode_file("main.py")</code>

<p>This will generate a main.myst file in order to execute myst file</p>

<code>Subdora.subdora_parse("main.myst")</code>

<h3>Additional features</h3>
<p>Subdora provide an iteration counter which ensures that .myst if parsing is done more than specified iterations Subdora automatically corrupt whole .myst file</p>

<code>Subdora.subdora_encode_file("main.py",no_of_iterations)</code>
