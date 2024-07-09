import React, { useEffect, useRef,useState } from 'react';
import Quill from 'quill';
import { marked } from 'marked';
import { useSelector, useDispatch } from 'react-redux';
import { updateContent } from '../features/article';
import ModifyPopover from './ModifyPopover';

function Article() {
    const editorRef = useRef(null);
    const popoverRef = useRef(null);
    const dispatch = useDispatch();
    const article = useSelector((state) => state.article.value);
    const [selectionRange, setSelectionRange] = useState(null);
    const [showMenu, setShowMenu] = useState(false);
    const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
    const [showPopover, setShowPopover] = useState(false);

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
                toolbar: '#toolbar',
            }
        });
        editorRef.current.quill = quill;

        const initialDelta = {
            ops: [
                { insert: article.title, attributes: {bold:true, } },
                { insert: '\n' },
                ...Object.values(article.content).flatMap(section => [
                    { insert: section.title, attributes: { bold: true } },
                    { insert: '\n' },
                    ...Object.values(section.paragraphs).flatMap(paragraph => [
                        { insert: '        ' + paragraph.content },
                        { insert: '\n' }
                    ])
                ])
            ]
        };
        quill.setContents(initialDelta);
        quill.formatLine(0, 1, 'align', 'center');
        quill.on('text-change', (delta, oldDelta, source) => {
            if (source === 'user') {
                dispatch(updateContent(quill.getContents().ops));
            }
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
            <div id="toolbar">
                {/* <!-- Text styles --> */}
                <span className="ql-formats">
                    <button className="ql-bold"></button>
                    <button className="ql-italic"></button>
                    <button className="ql-underline"></button>
                    <button className="ql-strike"></button>
                </span>

                {/* <!-- Blocks --> */}
                {/* <span className="ql-formats">
                    <button className="ql-blockquote"></button>
                    <button className="ql-code-block"></button>
                </span> */}

                {/* <!-- Lists --> */}
                {/* <span className="ql-formats">
                    <button className="ql-list" value="ordered"></button>
                    <button className="ql-list" value="bullet"></button>
                    <button className="ql-list" value="check"></button>
                </span> */}

                {/* <!-- Indentation --> */}
                {/* <span className="ql-formats">
                    <button className="ql-indent" value="-1"></button>
                    <button className="ql-indent" value="+1"></button>
                </span> */}

                {/* <!-- Headers --> */}
                {/* <span className="ql-formats">
                    <select className="ql-header">
                        <option value="1"></option>
                        <option value="2"></option>
                        <option value="3"></option>
                        <option value="4"></option>
                        <option value="5"></option>
                        <option value="6"></option>
                        <option selected></option>
                    </select>
                </span> */}

                {/* <!-- Text Color and Background --> */}
                <span className="ql-formats">
                    <select className="ql-color"></select>
                    <select className="ql-background"></select>
                </span>

                {/* <!-- Font and Alignment --> */}
                <span className="ql-formats">
                    <select className="ql-align"></select>
                    <select className="ql-font"></select>
                </span>

                {/* <!-- Clean Formatting --> */}
                {/* <span className="ql-formats">
                    <button className="ql-clean"></button>
                </span> */}
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
                    className="modify-menu"
                    style={{
                        position: 'absolute',
                        top: menuPosition.y + 'px',
                        left: menuPosition.x + 'px',
                        display: 'block'
                    }}
                    onClick={handleMenuClick}
                >
                    AI润色
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

        </div>
    );
}

export default Article;
