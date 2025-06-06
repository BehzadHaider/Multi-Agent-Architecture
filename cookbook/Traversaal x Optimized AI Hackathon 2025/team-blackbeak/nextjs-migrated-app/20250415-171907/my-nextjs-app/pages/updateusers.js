import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Navigation from '../components/Navigation';
import Footer from '../components/Footer';

const UpdateUsers = ({ user, username }) => {
  const [formData, setFormData] = useState({
    name: user.name,
    gender: user.gender,
    username: user.username,
    password: user.password,
    address: user.address,
    email: user.email,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch(`/api/updateusers?id=${user.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (res.ok) {
      window.location.href = '/viewusers';
    }
  };

  return (
    <>
      <Header />
      <Navigation username={username} />
      <div className="content">
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input type="text" name="name" value={formData.name} onChange={handleChange} />
          </label>
          <br />
          <label>
            Gender:
            <input type="text" name="gender" value={formData.gender} onChange={handleChange} />
          </label>
          <br />
          <label>
            Username:
            <input type="text" name="username" value={formData.username} onChange={handleChange} />
          </label>
          <br />
          <label>
            Password:
            <input type="password" name="password" value={formData.password} onChange={handleChange} />
          </label>
          <br />
          <label>
            Address:
            <input type="text" name="address" value={formData.address} onChange={handleChange} />
          </label>
          <br />
          <label>
            Email:
            <input type="email" name="email" value={formData.email} onChange={handleChange} />
          </label>
          <br />
          <input type="submit" value="Submit" />
        </form>
      </div>
      <Footer />
    </>
  );
};

export async function getServerSideProps({ req, query }) {
  const { username } = req.session;

  if (!username) {
    return {
      redirect: {
        destination: '/',
        permanent: false,
      },
    };
  }

  const res = await fetch(`http://localhost:3000/api/viewusers?id=${query.id}`);
  const user = await res.json();

  return { props: { user, username } };
}

export default UpdateUsers;