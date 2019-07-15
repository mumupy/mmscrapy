# Sphinx安装使用

# sphinx安装
``` 
pip install sphinx sphinx-autobuild sphinx_rtd_theme
```

# 创建文档
``` 
cd docs
sphinx-quickstart
```

# 添加文档
在source目录添加hello.rst
``` 
hello,world
=============
```

同时在index.rst添加hello.rst文档
``` 
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   hello
```

在source/conf.py修改主题
``` 
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```

## 执行文档
``` 
make html
```