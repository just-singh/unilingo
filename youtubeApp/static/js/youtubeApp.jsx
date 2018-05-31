var React = require('react')
var ReactDOM = require('react-dom')
var classNames = require('classnames');
import {SimpleLineChart, SimplePieChart} from './graphs.jsx'

class StatsView extends React.Component{
  constructor(props){
    super(props);
    this.state = {
    }

    this.loadChannelStats = this.loadChannelStats.bind(this);
    this.loadChannelStats(this.props.channelId);
  }

  componentWillReceiveProps(nextProps) {
    this.loadChannelStats(nextProps.channelId);
  }

  loadChannelStats(channelId){
    $.ajax({
      type : 'GET',
      url : '/ajax/channel_stats/',
      data: {
        channel_id: channelId
      },
    }).then(function(data) {
      if(!data){
        alert("An error has occurred loading the channel data.")
      } else{
        console.log(data)
        console.log(data.subscriberCount)

        this.setState({data: data})
      }
    }.bind(this));

  }

  render() {
    var LIKE_DISLIKE_COLORS = ['#0088FE', '#00C49F']
    var COMMENT_VIEW_COLORS = ['#FFBB28', '#FF8042']

    return (
      <div>
        { this.state.data &&
          <React.Fragment>
          <div className="container">
            <div className="col-md-12">
              <div className="row">
                <div className="col-md-12">
                  <img className="channelThumb" src={this.state.data.thumb}/>
                  <h2 className="channelTitle">{this.state.data.title}</h2>
                  <p className="channelDescription">
                    {this.state.data.description}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="statsRow">
            <div className="container">
              <div className="row ">
                <div className="col-md-12">
                  <h3 className="statHeading"> This Channel Has</h3>
                </div>
              </div>
              <div className="row">
                <div className="col-md-3">
                  <p className="statValue">{this.state.data.viewCount }</p>
                  <p className="statType">
                    {this.state.data.viewCount == 1 ? 'View' : 'Views'}</p>
                </div>
                <div className="col-md-3">
                  <p className="statValue">{this.state.data.videoCount}</p>
                  <p className="statType">
                    {this.state.data.videoCount == 1 ? 'Video' : 'Videos'}</p>
                </div>
                <div className="col-md-3">
                  <p className="statValue">{this.state.data.subscriberCount}
                  </p>
                  <p className="statType">
                    {this.state.data.subscriberCount == 1 ?
                      'Subscriber' : 'Subscribers'}</p>
                </div>
                <div className="col-md-3">
                  <p className="statValue">{this.state.data.commentCount}</p>
                  <p className="statType">
                    {this.state.data.commentCount == 1 ? 'Comment' : 'Comments'}
                  </p>
                </div>
              </div>
            </div>
          </div>
          {(this.state.data.likeDislikeData ||
            this.state.data.commentViewData ||
            this.state.data.viewTimeData.length > 0) &&
            <div className="container sectionPadding">
              <div className="row">
                {this.state.data.likeDislikeData &&
                  <div className="col-md-6">
                    <h3 className="ratioHeading">Like to Dislike Ratio</h3>
                    <SimplePieChart data={this.state.data.likeDislikeData}
                      colors={LIKE_DISLIKE_COLORS}/>
                  </div>
                }
                {this.state.data.commentViewData &&
                  <div className="col-md-6">
                    <h3 className="ratioHeading">Comment to View Ratio</h3>
                    <SimplePieChart data={this.state.data.commentViewData}
                      colors={COMMENT_VIEW_COLORS}/>
                  </div>
                }
              </div>
              {this.state.data.viewTimeData.length > 0 &&
                <div className="row viewTimePadding">
                  <div className="col-md-12">
                    <h3 className="ratioHeading">Views Over Time</h3>
                    <SimpleLineChart data={this.state.data.viewTimeData}/>
                  </div>
                </div>
              }
            </div>
          }
          { this.state.data.commentList.length > 0 &&
            <div className="statsRow sectionPadding">
              <div className="container">
                <div className="row ">
                  <div className="col-md-12">
                    <h3 className="commentHeading">Comments</h3>
                    <p className="commentSubheading"><b>Note:</b> The channels
                      provided for the demo didn't have any comments. I pulled
                      these from a video on the English channel.</p>
                      <ul>
                        { this.state.data.commentList.map(
                          function(comment, index){
                          return (
                            <li key={ index } className="comment">
                              <div>
                                <img src={comment.thumb}
                                  className="commentThumb"/>
                                <span className="commentUsername">
                                  { comment.name }
                                </span>

                              </div>
                              <p>{comment.text}</p>
                            </li>
                          )})}
                      </ul>
                  </div>
                </div>
              </div>
            </div>
          }
          </React.Fragment>
        }
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

    $.ajax({
      type : 'GET',
      url : '/ajax/upload_video/',
      data: {
        'title': this.state.title,
        'description': this.state.description,
        'tags': this.state.tags
      },

    }).then(function(data) {
      if(!data){
        alert ("There's been an error uploading the video.")
      } else{
        console.log("Ajax returned.")
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
        <div className="form-group sectionPadding">
          <h2 className="uploadHeader"> Currently this demo is hardcoded to use
            a preset 5 second video (because the server is pretty weak).
          </h2>
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
      </form>
    )
  }
}


class YoutubeApp extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      pageView: 'statsBrian',
    };

    this.changePageView = this.changePageView.bind(this);
  }

  changePageView(newPageView){
    this.setState({pageView: newPageView})
  }

  render() {

    // In an actual larger program we'd want to get the available channels from
    // the server. Given there are only two it seems like overkill currently,
    // so I've just hardcoded them.
    var STATS_PAGE_BRIAN = 'statsBrian';
    var STATS_PAGE_HISTORIA = 'statsHistoria';
    var UPLOAD_PAGE = 'upload';
    var CHANNEL_ID_BRIAN = 'UC9hWF751ZD5Qsn0Ff-A_fMA'
    var CHANNEL_ID_HISTORIA = 'UCTe4kaxOjgTg8Y3AOhyXfVA'

    var uploadClasses = classNames('nav-item', 'nav-link', {
      'active' : this.state.pageView == UPLOAD_PAGE
    })
    var statsBrianClasses = classNames('nav-item', 'nav-link', {
      'active' : this.state.pageView == STATS_PAGE_BRIAN
    })
    var statsStepClasses = classNames('nav-item', 'nav-link', {
      'active' : this.state.pageView == STATS_PAGE_HISTORIA
    })

    return (

      <div>
        <a className="pageHeading" href="/">unilingo</a>
        <nav className="navbar navbar-expand-lg navbar-dark">
          <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div className="navbar-nav">
              <a className={ statsBrianClasses } href="#"
                onClick={(e)=> this.changePageView(STATS_PAGE_BRIAN)}>
                  View Brian Makse Stats</a>
              <a className={ statsStepClasses } href="#"
                onClick={(e)=> this.changePageView(STATS_PAGE_HISTORIA)}>
                View Step Back Historia Stats</a>
              <a className={ uploadClasses } href="#"
                onClick={(e)=> this.changePageView(UPLOAD_PAGE)}>Upload Video
                <span className="sr-only">(current)</span></a>
            </div>
          </div>
        </nav>

        {this.state.pageView == UPLOAD_PAGE ?
          <div className="container">
            <div className="col-md-12">
              <UploadView/>
            </div>
          </div>
        : this.state.pageView == STATS_PAGE_BRIAN ?
          <StatsView channelId={CHANNEL_ID_BRIAN}/>
        :
          <StatsView channelId={CHANNEL_ID_HISTORIA}/>
        }
      </div>
    )
  }
}

ReactDOM.render(<YoutubeApp />, document.getElementById('container'))
