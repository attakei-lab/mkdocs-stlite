# Home

This is MkDocs extension to integrate Stlite application from code-block.

## Usage

Write code block marked `stlite`.

````markdown
```stlite
---
requirements = ["matplotlib"]
---
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

size = st.slider("Sample size", 100, 1000)

arr = np.random.normal(1, 1, size=size)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
```
````

```stlite
---
requirements = ["matplotlib"]
---
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# NOTE: Requirement to keep page title
st.set_page_config(page_title="MkDocs-Stlite")

size = st.slider("Sample size", 100, 1000)

arr = np.random.normal(1, 1, size=size)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
```
