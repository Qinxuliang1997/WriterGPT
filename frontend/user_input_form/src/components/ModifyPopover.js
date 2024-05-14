import React, { useState } from 'react';
import axios from 'axios';
import { FaPaperPlane,FaSyncAlt } from 'react-icons/fa';
import { ClipLoader } from 'react-spinners';
import { useSelector } from 'react-redux';

const ModifyPopover = React.forwardRef(({ selectedText, onSubmit, onClose, style }, ref) => {
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [replacementText, setReplacementText] = useState(null);
    const [showReplacementOptions, setShowReplacementOptions] = useState(false);
    const description = useSelector((e) => e.description.value);

    const handleSubmit = () => {
        setIsLoading(true);
        axios.post('http://127.0.0.1:8000/api/modify/', Object.assign({
            originalText: selectedText,
            userInput: inputText,
            }, description),
            {
                headers: {
                  'Content-Type': 'application/json',
                }
            },
        )
        .then(response => {
            setIsLoading(false);
            setReplacementText(response.data.content);
            setShowReplacementOptions(true);
        })
        .catch(error => {
            setIsLoading(false);
            console.error('There was an error!', error);
        });
    };
    const handleReplaceClick = () => {
        if (replacementText) {
            onSubmit(replacementText);
            onClose();
        }
    };
    
    return (
        <div ref={ref} className="modifypopover" style={style}>
            <div className="modifytext">
                <blockquote style={{ margin: '0' }}>
                    {showReplacementOptions ? replacementText : selectedText}
                </blockquote>
            </div>
            <div className="modifyaction">
                {!showReplacementOptions ? (
                    <>
                        <input
                            type="text"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            placeholder='你希望如何更改这段话？'
                        />
                        {isLoading ? (
                            <ClipLoader size={24} />
                        ) : (
                            <FaPaperPlane onClick={handleSubmit} style={{ cursor: 'pointer' }} />
                        )}    
                    </>
                ) : (
                    <button onClick={handleReplaceClick} >
                        替换原文 <FaSyncAlt style={{ marginLeft: '5px' }} />
                    </button>
                )}
            </div>
        </div>
    );
});

export default ModifyPopover;
