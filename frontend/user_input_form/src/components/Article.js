import React, { useEffect, useRef } from 'react';
import Quill from 'quill';
import { useSelector, useDispatch } from 'react-redux';
import { fill } from '../features/content';

function Article() {
    const editorRef = useRef(null);
    const dispatch = useDispatch();
    const content = useSelector((e) => e.content.value.content);

    // 初始化编辑器的 useEffect
    useEffect(() => {
        const quill = new Quill(editorRef.current, {
            theme: 'snow'
        });
        const safeContent = typeof content === 'string' ? content : '';
        quill.clipboard.dangerouslyPasteHTML(safeContent);
        // 保存 Quill 实例到 ref 中，以便在组件外部使用
        editorRef.current.quill = quill;
        }, []);
    
    return (
        <div className="article-writer">
            <h2>Write a Article</h2>
            <div className="container">
                <div className="editor-container">
                    <div className="editor-wrapper">
                        <div ref={editorRef} className="editor"></div>
                        {/* <button onClick={sendQuestion}>
                            Write
                        </button> */}
                    </div>
                    {/* <div id="loading" className="loading"></div> */}
                </div>
            </div>
        </div>
    );
}

export default Article;
