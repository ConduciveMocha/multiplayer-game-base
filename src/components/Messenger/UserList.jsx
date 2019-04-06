import React from 'react';

const UserElement = (props) =>{
    return(
    <li onClick={props.onClickFunction}>
        <div>
            <div className="img-placeholder"></div>
            <p>props.username</p>
        </div>
    </li>)
}

const UserList = (props) => {
    const userElements = props.users.map(el => {
        <UserElement key={el.userId} username={el.username} onClickFunction={props.createOnClick(el.userId)}/>
    })

    return (
        <div className="userlist-container">
            <ul>
                {userElements}
            </ul>
        </div>
    )

}
export default UserList;