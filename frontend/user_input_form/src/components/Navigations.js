import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import React, { useState, useEffect} from 'react';

export function Navigation() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      setIsAuth(true);
    }
  }, [isAuth]);

  return (
    <Navbar className='navbar'>
        <Navbar.Brand href="/" className="navbarbrand">WanJuan GongWen</Navbar.Brand>
        
        <Nav className="me-auto">
        </Nav>

        <Nav>
        {isAuth ?
            null:
            <Nav.Link href='/register'>Register</Nav.Link>
        }          
        {isAuth ?
            <Nav.Link href="/logout">Logout</Nav.Link>:
            <Nav.Link href="/login">Login</Nav.Link>
        }
        </Nav>
    </Navbar>
  );
}

export default Navigation