import BASE_URL from "../../urls"
import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Container, Button } from "react-bootstrap";
import "./style.css";
import logo from '../../assets/logo.png';
import AuthInput from '../../components/AuthInput/index'
import axios from "axios";
import { useNavigate, useParams } from 'react-router-dom';


function Blog() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [creationDate, setCreationDate] = useState("")
  const [title, setTitle] = useState("")
  const [main_image, setMainImage] = useState("")
  const [introduction, setIntroduction] = useState("")

  const [heading1, setHeading1] = useState("")
  const [paragraph1, setParagraph1] = useState("")
  const [section_image1, setSectionImage1] = useState("")

  const [heading2, setHeading2] = useState("")
  const [paragraph2, setParagraph2] = useState("")
  const [section_image2, setSectionImage2] = useState("")

  const [conclusion, setConclusion] = useState("")
  const [token, setToken] = useState("")

  const [likes_count, setLikesCount] = useState(22)
  const [likeStatus, setLikeStatus] = useState(false);

  const [restaurant_id , setRestaurantID] = useState("")
  const [restaurant_logo, setRestaurantLogo] = useState("")


  function fetchLikeCount() {
    const token = localStorage.getItem("user_token");

    axios({
      method: 'GET',
      url: BASE_URL + `/blogs/${id}/likes/amount/`,
      headers: {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
      },
      data: {}
    }).then((res) => {
      console.log(res.data)
      setLikesCount(res.data["like_count"])
    }).catch((err) => {
      if (err.response) {
        console.log(err.response.data);
      } else if (err.request) {
        console.log(err.request);
      } else {
        console.log(err.message);
      }
    });
    return
  }


  function fetchBlogDetails() {
    const token = localStorage.getItem("user_token");
    setToken(token)

    axios({
      method: 'Get',
      url: BASE_URL + '/blogs/' + id + '/details/',
      headers: {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
      },
    }).then((res) => {
      setTitle(res.data.title)
      setIntroduction(res.data.intro)
      setHeading1(res.data.heading1)
      setParagraph1(res.data.para1)
      setHeading2(res.data.heading2)
      setParagraph2(res.data.para2)

      setMainImage(res.data.main_image)
      setSectionImage1(res.data.section_image1)
      setSectionImage2(res.data.section_image2)

      setConclusion(res.data.conclusion)
      let d = new Date(res.data.created_at)
      setCreationDate(d.toString())

      // we have to fetch the restaurant image
      console.log(res.data)
      var rid = res.data.restaurant_id
      axios({
        method: 'GET',
        url: BASE_URL + `/restaurants/${rid}/view/`,
        headers: {
          'authorization': 'Bearer ' + token,
          'content-type': 'application/json'
        },
        data: {}
      }).then((res) => {
        console.log(res.data)
        setRestaurantID(res.data.id)
        setRestaurantLogo(res.data.logo)

      }).catch((err) => {
        if (err.response) {
          console.log(err.response.data);
        } else if (err.request) {
          console.log(err.request);
        } else {
          console.log(err.message);
        }
      });


    }).catch((err) => {
      console.log(err)
      navigate("/Login")


    })
  }


  function fetchLikeStatus() {
    const token = localStorage.getItem("user_token");
    axios({
      method: 'GET',
      url: BASE_URL + `/blogs/${id}/liked/`,
      headers: {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
      },
      data: {}
    }).then((res) => {
      console.log(res.data)
      setLikeStatus(res.data["liked"] === 'True')
    }).catch((err) => {
      if (err.response) {
        console.log(err.response.data);
      } else if (err.request) {
        console.log(err.request);
      } else {
        console.log(err.message);
      }
    });
    return
  }

  useEffect(() => {
    if (!localStorage.getItem("user_token")) {
      console.log("no token")
      navigate("/Login");
    }

    fetchBlogDetails()
    fetchLikeCount()
    fetchLikeStatus()
  }, []);


  const handleLike = (e) => {
    const token = localStorage.getItem("user_token");
    axios({
      method: 'POST',
      url: BASE_URL + `/blogs/like/`,
      headers: {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
      },
      data: {
        blog_liked: id
      }
    }).then((res) => {
      setLikeStatus(true)
      fetchLikeCount()
      console.log("blog Liked");
    }).catch((err) => {
      if (err.response) {
        console.log(err.response.data);
      } else if (err.request) {
        console.log(err.request);
      } else {
        console.log(err.message);
      }
    })

    return false
  }

  const handleUnlike = (e) => {
    const token = localStorage.getItem("user_token");
    axios({
      method: 'DELETE',
      url: BASE_URL + `/blogs/${id}/unlike/`,
      headers: {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
      },

    }).then((res) => {
      setLikeStatus(false);
      fetchLikeCount()
      console.log("blog Unliked");
    }).catch((err) => {
      if (err.response) {
        console.log(err.response.data);
      } else if (err.request) {
        console.log(err.request);
      } else {
        console.log(err.message);
      }
    })

    return false
  }

  const handleLikeClick = (e) => {
    if (likeStatus) {
      handleUnlike()
    }
    handleLike()
  }



  return (<>
    <Container className="container mt-5">
      <div className="row">
        <div className="col-lg-8">
          <article>
            <header className="mb-4">
              <h1 className="fw-bolder mb-1">{title}</h1>
              <div className="text-muted fst-italic mb-2">
                {creationDate}:
                <a className="btn-link" href={`/restaurant/${restaurant_id}`}>
                  <img
                    id="restaurant_logo"
                    src={restaurant_logo}
                    alt="Miku logo" />
                </a>
              </div>

              <div className="text-muted blog-icons">
                <div>
                  <i className="btn-link far fa-thumbs-up" onClick={handleLikeClick}></i> {likes_count}
                </div>
                <div>
                  <a href="#comment-section">
                    <i className="btn-link far fa-comment fa-lg"></i> 2
                  </a>
                </div>

              </div>

            </header>
            <figure className="mb-4"><img className="img-fluid rounded" src={main_image} alt="..." /></figure>

            <section className="mb-5">
              <p className="card-text">
                {introduction}
              </p>

              <h2>{heading1}</h2>
              <figure className="mb-4"><img className="img-fluid rounded" src={section_image1} alt="..." /></figure>
              <p className="card-text">
                {paragraph1}
              </p>

              <h2>{heading2}</h2>
              <figure className="mb-4"><img className="img-fluid rounded" src={section_image2} alt="..." /></figure>
              <p className="card-text">
                {paragraph2}
              </p>

              <p>
                {conclusion}
              </p>
            </section>
          </article>
          <section className="mb-5" id="comment-section">
            <div className="card bg-light">
              <div className="card-body">
                <div className="d-flex flex-column comment-section">
                  <div className="bg-white p-2">
                    <div className="d-flex flex-row user-info"><img id="comment-logo" className="rounded-circle"
                      src="https://upload.wikimedia.org/wikipedia/commons/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg"
                      width="50px" height="50px" />
                      <div className="d-flex flex-column justify-content-start ml-2"><span
                        className="d-block font-weight-bold name">Elon Tusk</span><span className="date text-black-50">Shared
                          publicly - Jan 2020</span></div>
                    </div>
                    <div className="mt-2">
                      <p className="comment-text">A superb experience at Miku!
                        I love this stuff, even though it hurts my wallet.
                        The sushi there is always fresh and although sometimes
                        the combo may seem weird, the chefs know what they're
                        doing and the umami and taste just flow on the tongue.
                      </p>
                    </div>
                  </div>
                  <div className="bg-white">
                    <div className="d-flex flex-row fs-12">
                      <div className="like p-2 cursor"><i className="fa fa-thumbs-o-up"></i><span className="ml-1">Like</span></div>
                      <div className="like p-2 cursor"><i className="fa fa-commenting-o"></i><span className="ml-1">Comment</span>
                      </div>
                      <div className="like p-2 cursor"><i className="fa fa-share"></i><span className="ml-1">Share</span></div>
                    </div>
                  </div>
                  <div className="bg-light p-2">
                    <div className="d-flex flex-row align-items-start"><img id="comment-logo" className="rounded-circle"
                      src="https://m.media-amazon.com/images/M/MV5BYTNlOGZhYzgtMmE3OC00Y2NiLWFhNWQtNzg5MjRhNTJhZGVmXkEyXkFqcGdeQXVyNzg5MzIyOA@@._V1_.jpg"
                      width="50px" height="50px" /><textarea className="form-control ml-1 shadow-none textarea"></textarea>
                    </div>
                    <div className="mt-2 text-right"><button className="btn btn-sm shadow-none" type="button">Post
                      comment</button>
                      <button className="btn btn-sm ml-1 shadow-none" type="button">Cancel</button>
                    </div>

                  </div>
                </div>

              </div>
            </div>
          </section>
        </div>
        <div className="col-lg-4">
          <div className="card mb-4">
            <div className="card-header">Search</div>
            <div className="card-body">
              <div className="input-group">
                <input className="form-control" type="text" placeholder="Enter search term..."
                  aria-label="Enter search term..." aria-describedby="button-search" />
                <button className="btn btn" id="button-search" type="button">Go!</button>
              </div>
            </div>
          </div>
          <div className="card mb-4">
            <div className="card-header">Similar Categories</div>
            <div className="card-body">
              <div className="row">
                <div className="col-sm-6">
                  <ul className="list-unstyled mb-0">
                    <li><a href="#!">Seafood</a></li>
                    <li><a href="#!">Canada</a></li>
                    <li><a href="#!">Asian</a></li>
                  </ul>
                </div>
                <div className="col-sm-6">
                  <ul className="list-unstyled mb-0">
                    <li><a href="#!">Japanese</a></li>
                    <li><a href="#!">Sushi</a></li>
                    <li><a href="#!">Aburi</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </Container>


  </>
  );

}

export default Blog