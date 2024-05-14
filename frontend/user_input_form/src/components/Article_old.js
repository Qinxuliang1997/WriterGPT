import React, { useEffect, useRef } from 'react';
import Quill from 'quill';
import { marked } from 'marked';
import { useSelector, useDispatch } from 'react-redux';
// import { fill } from '../features/content';

function Article() {
    const editorRef = useRef(null);
    // const dispatch = useDispatch();
    const content = useSelector((e) => e.content.value.content);

    // 初始化编辑器的 useEffect
    useEffect(() => {
        const quill = new Quill(editorRef.current, {
            theme: 'snow',
            modules: {
                toolbar: '#toolbar',
              }
        });
        const safeContent = typeof content === 'string' ? content : '';
        const htmlContent = marked(safeContent);
        quill.clipboard.dangerouslyPasteHTML(htmlContent);
        editorRef.current.quill = quill;
        }, []);
    
    return (
        <div className="article-writer">
            <div id="toolbar">
                {/* <!-- Text styles --> */}
                <span class="ql-formats">
                    <button class="ql-bold"></button>
                    <button class="ql-italic"></button>
                    <button class="ql-underline"></button>
                    <button class="ql-strike"></button>
                </span>

                {/* <!-- Blocks --> */}
                <span class="ql-formats">
                    <button class="ql-blockquote"></button>
                    <button class="ql-code-block"></button>
                </span>

                {/* <!-- Lists --> */}
                <span class="ql-formats">
                    <button class="ql-list" value="ordered"></button>
                    <button class="ql-list" value="bullet"></button>
                    <button class="ql-list" value="check"></button>
                </span>

                {/* <!-- Indentation --> */}
                <span class="ql-formats">
                    <button class="ql-indent" value="-1"></button>
                    <button class="ql-indent" value="+1"></button>
                </span>

                {/* <!-- Headers --> */}
                <span class="ql-formats">
                    <select class="ql-header">
                        <option value="1"></option>
                        <option value="2"></option>
                        <option value="3"></option>
                        <option value="4"></option>
                        <option value="5"></option>
                        <option value="6"></option>
                        <option selected></option>
                    </select>
                </span>

                {/* <!-- Text Color and Background --> */}
                <span class="ql-formats">
                    <select class="ql-color"></select>
                    <select class="ql-background"></select>
                </span>

                {/* <!-- Font and Alignment --> */}
                <span class="ql-formats">
                    <select class="ql-font"></select>
                    <select class="ql-align"></select>
                </span>

                {/* <!-- Clean Formatting --> */}
                <span class="ql-formats">
                    <button class="ql-clean"></button>
                </span>
            </div>

            <div className="container">
                <div className="editor-container">
                    <div className="editor-wrapper">
                        <div ref={editorRef} className="editor"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Article;
