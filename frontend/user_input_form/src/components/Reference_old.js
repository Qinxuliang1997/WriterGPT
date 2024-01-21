import React, { useState, useRef, useEffect } from "react";
import * as LR from "@uploadcare/blocks";
import { PACKAGE_VERSION } from "@uploadcare/blocks/env";
LR.registerBlocks(LR);

const Reference = () => {

  const dataOutputRef = useRef(null);
  const [files, setFiles] = useState([]);

  const handleUploaderEvent = (event) => {
    const { detail: { data } } = event;
    setFiles(data);
  };

  useEffect(() => {
    const el = dataOutputRef.current;
    if (el) {
      el.addEventListener("lr-data-output", handleUploaderEvent);
    }
    return () => {
      if (el) {
        el.removeEventListener("lr-data-output", handleUploaderEvent);
      }
    };
  }, [dataOutputRef]);

  return (
    <div>
      <h2>Article Reference</h2>
      <section
        // style={{
        //   "--uploadcare-pubkey": process.env.REACT_APP_VITE_UPLOADCARE_API_KEY,
        // }}
      >
        <lr-config
            ctx-name="my-uploader"
            pubkey="99c65c01fe9d7fed11d8"
            img-only="false"
            multiple="true"
            max-local-file-size-bytes="524288000"
            source-list="local, url, evernote"
        >
        </lr-config>
        <lr-file-uploader-inline
          ctx-name="my-uploader"
          css-src={`https://cdn.jsdelivr.net/npm/@uploadcare/blocks@${PACKAGE_VERSION}/web/lr-file-uploader-inline.min.css`}
        >
        </lr-file-uploader-inline>
        <lr-data-output
            ctx-name="my-uploader"
            ref={dataOutputRef}
            use-event
            hidden
            onEvent={handleUploaderEvent}
        />
        {/* <div className="file-gallery">
          {files.map((file) => (
            <p key={file.uuid}>{file.name}</p>
          ))}
        </div> */}
      </section>

    </div>

  );
};

export default Reference;