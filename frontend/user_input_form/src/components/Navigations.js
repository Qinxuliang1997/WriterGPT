import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import React, { useState, useEffect} from 'react';
import axios from 'axios';

export function Navigation() {
  const [isAuth, setIsAuth] = useState(false);

  // useEffect(() => {
  //   if (localStorage.getItem('access_token') !== null) {
  //     setIsAuth(true);
  //   }
  // }, []);
  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      axios
        .post(
          'http://106.14.184.241/token/verify/', 
          { token: accessToken }, 
          { headers: { Authorization: `Bearer ${accessToken}` } }
        )
        .then(response => {
          if (response.status === 200) {
            setIsAuth(true);
          }
        })
        .catch(error => {
          console.error('Token is invalid or expired', error);
          localStorage.removeItem('access_token');
          setIsAuth(false);
        });
    }
  }, []);

  return (
    <Navbar className='navbar'>
        <Container>
            <Navbar.Brand href="/">
              <img
                src="/logo.svg"
                width="30"
                height="30"
                className="d-inline-block align-top"
                alt="万卷"
              />
            </Navbar.Brand>
            {/* <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                万卷公文
              </Navbar.Text>
          </Navbar.Collapse> */}
            <Nav className="me-auto">
              <Nav.Link href="/start" className="auth-link">开始</Nav.Link>
              {/* <Nav.Link href="/start" className="auth-link">开始</Nav.Link>
              <Nav.Link href="/start" className="auth-link">教程</Nav.Link>
              <Nav.Link href="/start" className="auth-link">联系</Nav.Link> */}
            </Nav>
            <Navbar.Toggle/>
            <Navbar.Collapse id="responsive-navbar-nav">
              <Nav className="me-auto">
              </Nav>
              <Nav>
                {isAuth ? (
                  <Nav.Link href="/logout" className="auth-link">退出登录</Nav.Link>
                ) : (
                  <>
                    <Nav.Link href="/login" className="auth-link">登录</Nav.Link>
                    <Nav.Link href='/register' className="auth-link">注册</Nav.Link>
                  </>
                )}
              </Nav>              
            </Navbar.Collapse>
        </Container>
    </Navbar>
  );
}

export default Navigation