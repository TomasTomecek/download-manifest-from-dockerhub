# download-manifest.py

This is a simple script to download manifests from Docker hub. It is done via this v2 registry API call:

```
/v2/{repository}/manifests/{tag}
```

Sample usage:

```
$ ./download-manifest.py registry
{
  "schemaVersion": 1,
  "fsLayers": [
    {
      "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
    },
    {
      "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
    },
...
```

For more information check [this blog post](http://blog.tomecek.net/post/download-manifests-from-docker-hub/)
.
