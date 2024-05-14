import React, { useEffect, useRef, useState } from 'react';
import Quill from 'quill';
import { marked } from 'marked';
import { useSelector } from 'react-redux';
import axios from 'axios';

function Article() {
    const editorRef = useRef(null);
    const [showMenu, setShowMenu] = useState(false);
    const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
    const [prompt, setPrompt] = useState('');
    const [replacementText, setReplacementText] = useState('');
    const [selectionRange, setSelectionRange] = useState(null);
    const content = useSelector((e) => e.content.value.content);

    useEffect(() => {
        if (editorRef.current) {
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

            quill.on('selection-change', (range) => {
                if (range) {
                    if (range.length === 0) {
                        setShowMenu(false);
                    } else {
                        const bounds = quill.getBounds(range);
                        setMenuPosition({ x: bounds.left, y: bounds.top });
                        setSelectionRange(range);
                        setShowMenu(true);
                    }
                } else {
                    setShowMenu(false);
                }
            });
        }
    }, [content]);

    function handleMenuClick() {
        alert('You clicked me!');
        // event.stopPropagation();
        console.log('good')
        const text = prompt("Please enter your LLM prompt:");
        if (text && selectionRange) {
            const quill = editorRef.current.quill;
            const selectedText = quill.getText(selectionRange.index, selectionRange.length);
            try {
                const response = axios.post('/api/modify-text', {
                    text: selectedText,
                    prompt: text
                });
                setReplacementText(response.data.modifiedText);
                setPrompt(text);
            } catch (error) {
                console.error('Error fetching data: ', error);
            }
        }
        setShowMenu(false);
    };

    const handleFillClick = () => {
        if (replacementText && selectionRange) {
            const quill = editorRef.current.quill;
            quill.deleteText(selectionRange.index, selectionRange.length);
            quill.insertText(selectionRange.index, replacementText);
            setReplacementText('');
        }
    };

    return (
        <div className="article-writer">
            <div id="toolbar">...toolbar buttons...</div>
            <div className="container">
                <div className="editor-container">
                    <div className="editor-wrapper">
                        <div ref={editorRef} className="editor"></div>
                    </div>
                </div>
            </div>
            {showMenu && (
                <div
                    className="modify-menu"
                    style={{
                        top: menuPosition.y + 'px',
                        left: menuPosition.x + 'px'
                    }}
                    onClick={handleMenuClick}
                >
                    Modify
                </div>
            )}
            {replacementText && (
                <div className="replacement-text">
                    <p>{replacementText}</p>
                    <button onClick={handleFillClick}>Fill</button>
                </div>
            )}
        </div>
    );
}

export default Article;
