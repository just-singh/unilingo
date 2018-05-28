var React = require('react')
var ReactDOM = require('react-dom')
var classNames = require('classnames');
import { BarChart, Bar, XAxis, YAxis } from 'recharts';


class StatsView extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      data : [
            {name: 'Page A', uv: 4000, pv: 2400, amt: 2400},
            {name: 'Page B', uv: 3000, pv: 1398, amt: 2210},
            {name: 'Page C', uv: 2000, pv: 9800, amt: 2290},
            {name: 'Page D', uv: 2780, pv: 3908, amt: 2000},
            {name: 'Page E', uv: 1890, pv: 4800, amt: 2181},
            {name: 'Page F', uv: 2390, pv: 3800, amt: 2500},
            {name: 'Page G', uv: 3490, pv: 4300, amt: 2100},
      ],
    }
  }

  render() {
    return (
      <div>
        <p> Statistics View</p>
        <BarChart width={600} height={300} data={this.state.data}>
          <XAxis dataKey="name"  />
          <YAxis />
          <Bar type="monotone" dataKey="uv" barSize={30} fill="#8884d8"
            />
        </BarChart>
      </div>
    )
  }
}

class UploadView extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      title: '',
      description: '',
      tags: '',
      fileInput: '',
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }

  handleSubmit(event) {
    event.preventDefault();
    alert(
      `Selected file - ${this.fileInput.files[0].name}`
    );

    $.ajax({
      type : 'GET',
      url : '/upload/ajax/',
      data: {
      },
    }).then(function(data) {
      if(!data){
        alert ("There's been an error uploading the video.")
      } else{
        //this.setState({pageView: 'success'})
      }
    }.bind(this));

  }

  handleChange(event){
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="form-group">
          <label htmlFor="vidFile">Select a video to upload.</label>
          <input name="vidFile" id="vidFile"
            ref={input => {
              this.fileInput = input;
            }}
            className="form-control-file" type="file"/>
        </div>

        <div className="form-group">
          <label htmlFor="vidTitle">Title</label>
          <input type="title" className="form-control" id="vidTitle"
            name="title"
            value={this.state.title}
            onChange={this.handleChange}
            placeholder="Enter a title for the video."/>
        </div>

        <div className="form-group">
          <label htmlFor="vidTags">Tags</label>
          <input type="tags" className="form-control" id="vidTags"
            name="tags"
            value={this.state.tags}
            onChange={this.handleChange}
            placeholder="Enter tags for the video (comma separated list)"/>
        </div>

        <div className="form-group">
          <label htmlFor="vidDesc">Description</label>
          <textarea placeholder="Enter a description for the video"
            name="description"
            value={this.state.description}
            onChange={this.handleChange}
            className="form-control" id="vidDesc" rows="3"></textarea>
        </div>

        <button type="submit" className="btn btn-primary">Upload Video
        </button>

        <p>{this.state.title}</p>
        <p>{this.state.tags}</p>
        <p>{this.state.description}</p>

      </form>
    )
  }
}

class YoutubeApp extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      pageView: 'upload',
    };

    this.changePageView = this.changePageView.bind(this);
  }

  changePageView(newPageView){
    this.setState({pageView: newPageView})
  }

  render() {
    var statsPage = 'stats';
    var uploadPage = 'upload';

    var uploadClasses = classNames('nav-item', 'nav-link', {
      'active' : this.state.pageView == uploadPage
    })
    var statsClasses = classNames('nav-item', 'nav-link', {
      'active' : this.state.pageView == statsPage
    })

    return (

      <div>
        <h1 className="pageHeading">Unilingo Youtube App</h1>

        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div className="navbar-nav">
              <a className={ uploadClasses } href="#"
                onClick={(e)=> this.changePageView(uploadPage)}>Upload Video
                <span className="sr-only">(current)</span></a>
              <a className={ statsClasses } href="#"
                onClick={(e)=> this.changePageView(statsPage)}>View Statistics</a>
            </div>
          </div>
        </nav>

        <div className="container">
          <div className="col-md-12">
            {this.state.pageView == 'upload' ?
              <UploadView/>
            :
              <StatsView/>
            }
          </div>
        </div>
      </div>
    )
  }
}

ReactDOM.render(<YoutubeApp />, document.getElementById('container'))
