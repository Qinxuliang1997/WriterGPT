import React, { useEffect, useRef,useState } from 'react';
import Quill from 'quill';
import { marked } from 'marked';
import { useSelector, useDispatch } from 'react-redux';
import { updateContent } from '../features/article';
import ModifyPopover from './ModifyPopover';
import axios from 'axios';

const Inline = Quill.import('blots/inline');

class OriginText extends Inline {
    static create(value) {
        let node = super.create(value);
        node.setAttribute('style', 'text-decoration: none; color: #3D5272FC; background-color:none');
        return node;
    }
}

OriginText.blotName = 'origin';
OriginText.tagName = 'ori';

Quill.register(OriginText);

class DeletedText extends Inline {
    static create(value) {
      let node = super.create(value);
      node.setAttribute('style', 'text-decoration: line-through; color: red; background-color:none');
      return node;
    }
  }
  
  DeletedText.blotName = 'deleted';
  DeletedText.tagName = 'del';
  
  Quill.register(DeletedText);
  
  // 自定义新增文本格式
  class AddedText extends Inline {
    static create(value) {
      let node = super.create(value);
      node.setAttribute('style', 'text-decoration: none; color: green; background-color: lightgreen');
      return node;
    }
  }
  
  AddedText.blotName = 'added';
  AddedText.tagName = 'ins';

  Quill.register(AddedText)

function Article() {
    const editorRef = useRef(null);
    const popoverRef = useRef(null);
    const dispatch = useDispatch();
    const article = useSelector((state) => state.article.value);
    const [selectionRange, setSelectionRange] = useState(null);
    const [showMenu, setShowMenu] = useState(false);
    const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
    const [showPopover, setShowPopover] = useState(false);
    const [isLoadingProofread, setIsLoadingProofread] = useState(false);
    const [errorProofread, setErrorProofread] = useState('');

    useEffect(() => {
        function handleClickOutside(event) {
            if (popoverRef.current && !popoverRef.current.contains(event.target)) {
                console.log("Click was outside ModifyPopover, showPopover is", showPopover);
                if (showPopover) {
                    setShowPopover(false);
                }
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [showPopover]);

    useEffect(() => {
        if (!editorRef.current) return;
        const quill = new Quill(editorRef.current, {
            theme: 'snow',
            modules: {
                toolbar: {
                  container: '#toolbar',
                  handlers: {
                    // Add custom undo and redo functionality
                    undo: function() {
                      this.quill.history.undo();
                    },
                    redo: function() {
                      this.quill.history.redo();
                    }
                  }
                },
                history: {
                  delay: 2000,
                  maxStack: 500,
                  userOnly: true
                }
            },
            // modules: {
            //     toolbar: '#toolbar',
            // }
        });
        editorRef.current.quill = quill;

        // const initialDelta = {
        //     ops: [
        //         { insert: article.title, attributes: {bold:true, } },
        //         { insert: '\n' },
        //         { insert: article.title },
        //         { insert: '\n', attributes: { header: 1 } },
        //         ...Object.values(article.content).flatMap(section => [
        //             { insert: section.title, attributes: { bold: true } },
        //             { insert: '\n' },
        //             ...Object.values(section.paragraphs).flatMap(paragraph => [
        //                 { insert: '        ' + paragraph.content },
        //                 { insert: '\n' }
        //             ])
        //         ])
        //     ]
        // };
        const initialDelta = {
            ops: [
                // { insert: article.title },
                // { insert: '\n', attributes: { header: 3 } },
                ...(article.title ? [{ insert: article.title }, { insert: '\n', attributes: { header: 3 } }] : []),
                ...Object.values(article.content).flatMap(section => [
                    // { insert: section.title},
                    // { insert: '\n', attributes: { header: 4 } },
                    ...(section.title ? [{ insert: section.title }, { insert: '\n', attributes: { header: 4 } }] : []),
                    ...Object.values(section.paragraphs).flatMap(paragraph => [
                        { insert: paragraph.content },{ insert: '\n' }
                    ])
                ])
            ]
        };
        quill.setContents(initialDelta);
        // quill.formatLine(0, 1, 'align', 'center');
        const wordCount = quill.getLength();
        document.getElementById('word-count').innerText = `${wordCount} 字`;
        quill.on('text-change', (delta, oldDelta, source) => {
            if (source === 'user') {
                dispatch(updateContent(quill.getContents().ops));
            }
            const wordCount = quill.getLength();
            document.getElementById('word-count').innerText = `${wordCount} 字`;
        });
        quill.on('selection-change', (range) => {
            if (range) {
                if (range.length === 0) {
                    setShowMenu(false);
                } else {
                    const text = quill.getText(range.index, range.length);
                    console.log('User has highlighted', text);
                    const bounds = quill.getBounds(range);
                    const editorBounds = editorRef.current.getBoundingClientRect();
                    // Add scroll positions
                    const scrollTop = editorRef.current.scrollTop;
                    const scrollLeft = editorRef.current.scrollLeft;
                    setMenuPosition({
                        x: bounds.left + editorBounds.left - scrollLeft,
                        y: bounds.top + editorBounds.top - scrollTop
                    });
                    setSelectionRange(range);
                    setShowMenu(true);
                }
            } else {
                setShowMenu(false);
            }
        });
        document.getElementById('copy-button').addEventListener('click', function () {
            const editorText = quill.getText();
            // copyToClipboard(editorText)
            navigator.clipboard.writeText(editorText).then(() => {
                alert('文本已复制到剪切板');
            });
        });

        
        function handleProofread() {
            setIsLoadingProofread(true);
            setErrorProofread('');
            const quill = editorRef.current.quill;
            const originalText = quill.getText();

            axios.post('http://106.14.184.241/api/proofread/', 
                { text: originalText },
                {
                    headers: {
                    'Content-Type': 'application/json',
                    },
                })
            .then(response => {
                const diffs = response.data.content; // Assuming the proofread text is returned under 'text' key
                // const diffs = diffChars(originalText, proofreadText)
                console.log(diffs);
                quill.deleteText(0, quill.getLength(), Quill.sources.SILENT);
                let index = 0;
                diffs.forEach(diff => {
                    const operation = diff[0]; // 获取操作符（第一个字符）
                    const text = diff.slice(2); // 获取文本（去除操作符和空格）
                    if (operation === ' ') {                     
                        quill.insertText(index, text, {'deleted': false, 'added': false, 'origin': true});
                        index += text.length;
                    } else if (operation === '+') { 
                        quill.insertText(index, text, {'deleted': false, 'added': true, 'origin': false});
                        index += text.length;
                    } else if (operation === '-') {
                        quill.insertText(index, text, {'deleted': true, 'added': false, 'origin': false});
                        index += text.length;
                    }
                });
                setIsLoadingProofread(false)
            })
            .catch(error => {
                console.error('Proofreading failed:', error);
                setErrorProofread('校对失败，请重试。');
                setIsLoadingProofread(false);
            });
        }

        // Add a custom blot to handle proofreading hover
        // Quill.register('formats/proofread', ProofreadBlot);

        // Add the proofread button event listener
        document.getElementById('proofread-button').addEventListener('click', handleProofread);

        return () => {
            quill.off('text-change');
            quill.off('selection-change');
        };
        }, []);
    
    function handleMenuClick() {
        setShowPopover(true);
        console.log('click modify');
        console.log('After setting showPopover: ', showPopover);
    };

    function handleTextSubmit(text) {
        const quill = editorRef.current.quill;
        const range = quill.getSelection(true);
        if (text) {
            quill.deleteText(range.index, range.length);
            quill.insertText(range.index, text);
        }
        setShowPopover(false);
    }

    return (
        <div className="article-writer">
            <div id="toolbar-container" className="custom-toolbar">
                <div id="toolbar" className="ql-toolbar ql-snow">
                    {/* <!-- Headers --> */}
                    <span className="ql-formats">
                        <select className="ql-header">
                            <option value="1"></option>
                            <option value="2"></option>
                            <option value="3"></option>
                            <option value="4"></option>
                            <option value="5"></option>
                            <option value="6"></option>
                            <option selected></option>
                        </select>
                    </span>
                    <span className="divider"></span>

                    {/* <!-- Text styles --> */}
                    <span className="ql-formats">
                        <button className="ql-bold"></button>
                        <button className="ql-italic"></button>
                        <button className="ql-underline"></button>
                        <button className="ql-strike"></button>
                        {/* <button className="ql-blockquote"></button> */}
                        {/* <button className="ql-code-block"></button> */}
                        <select className="ql-color"></select>
                        <select className="ql-background"></select>
                    </span>
                    <span className="divider"></span>

                    {/* <!-- Font and Alignment --> */}
                    <span className="ql-formats">
                        <select className="ql-align"></select>
                        <button className="ql-indent" value="-1"></button>
                        <button className="ql-indent" value="+1"></button>
                        {/* <button className="ql-list" value="ordered"></button>
                        <button className="ql-list" value="bullet"></button>
                        <button className="ql-list" value="check"></button>                     */}
                    </span>
                    <span className="divider"></span>

                    {/* <!-- Indentation --> */}
                    {/* <span className="ql-formats">
                        <button className="ql-indent" value="-1"></button>
                        <button className="ql-indent" value="+1"></button>
                    </span> */}

                    {/* <!-- Text Color and Background --> */}
                    {/* <span className="ql-formats">
                        <select className="ql-color"></select>
                        <select className="ql-background"></select>
                    </span> */}

                    {/* <!-- Clean Formatting --> */}
                    {/* <span className="ql-formats">
                        <button className="ql-clean"></button>
                    </span> */}
                    {/* <!-- Undo and Redo buttons --> */}
                    <span className="ql-formats">
                        <button className="ql-undo">
                            {/* <i className="fa fa-undo"></i></button> */}
                            <img src="/undo.svg" alt="Undo" className="svg-icon" />
                            </button>
                        <button className="ql-redo">
                            {/* <i className="fa fa-redo"></i> */}
                            <img src="/redo.svg" alt="Redo" className="svg-icon" />
                        </button>
                    </span>
                </div>  
                <div class="toolbar-right">
                    <span id="word-count">0 字</span>
                    <button id="copy-button">复制</button>
                    <button id="proofread-button">校对</button>
                </div>              
            </div>

            <div className="container">
                <div className="editor-container">
                    <div className="editor-wrapper">
                        <div ref={editorRef} className="editor"></div>
                    </div>
                </div>
            </div>

            {showMenu && (
                <button
                // <div
                    className="modify-menu"
                    style={{
                        position: 'absolute',
                        top: menuPosition.y + 'px',
                        left: menuPosition.x + 'px',
                        display: 'block'
                    }}
                    onClick={handleMenuClick}
                >
                    <span style={{ opacity: 0 }}>Clickable area</span>
                {/* // </div> */}
                {/* > */}
                {/* //     AI润色 */}
                </button>
            )}
            {showPopover && (
                <ModifyPopover
                    ref={popoverRef}
                    selectedText={editorRef.current.quill.getText(selectionRange.index, selectionRange.length)}
                    onSubmit={handleTextSubmit}
                    onClose={() => setShowPopover(false)}
                    style={{
                        position: 'absolute',
                        top: menuPosition.y + 10 + 'px',
                        left: menuPosition.x + 'px'
                    }}
                />
            )}

            {isLoadingProofread && (
                <div className="loading-overlay">
                    正在校对中，请稍候...
                </div>
                )}
                {errorProofread && (
                    <div className="error-message">
                        {errorProofread}
                    </div>
            )}
        </div>
    );
}

export default Article;
