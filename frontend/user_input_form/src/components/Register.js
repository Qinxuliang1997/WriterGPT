import axios from "axios";
import {Navigate} from "react-router-dom";
import {useState} from "react";

export const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const submit = async e => {
        e.preventDefault();

        const user = {
            username: username,
            password: password
          };
        
        try {
        // localhost:8000
            const {data} = await axios.post('http://106.14.184.241/register/', user ,{headers: {
                'Content-Type': 'application/json'
            }}, {withCredentials: true});

            console.log(data)
            window.location.href = '/login'
        } catch (error) {
            if (error.response && error.response.status === 401) {
                setError('注册失败，请稍候再试');
            } else {
                setError('注册失败，请稍后再试');
            }
        }
    }

    return(
        <div className="Auth-form-container">
            <form className="Auth-form" onSubmit={submit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">注册</h3>
                    {error && <div className="alert alert-danger" role="alert">{error}</div>}
                    <div className="form-group mt-3">
                        <label>用户名</label>
                        <input
                            className="form-control mt-1"
                            // placeholder="输入用户名"
                            name='username'
                            type='text'
                            value={username}
                            required
                            onChange={e => setUsername(e.target.value)}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>密码</label>
                        <input
                            name='password'
                            type="password"
                            className="form-control mt-1"
                            // placeholder="输入密码"
                            value={password}
                            required
                            onChange={e => setPassword(e.target.value)}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            提交
                        </button>
                    </div>
                </div>
            </form>
        </div>
    )
}

export default Register