var React = require('react')
var ReactDOM = require('react-dom')
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell } from 'recharts';

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius,
  percent, index }) => {
 	const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x  = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy  + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'}
      dominantBaseline="central">
    	{`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};


export class SimpleLineChart extends React.Component{
	render () {
    var data = this.props.data
  	return (
    	<LineChart width={800} height={400} data={data}
            margin={{top: 5, right: 30, left: 20, bottom: 5}}>
       <XAxis dataKey="date"/>
       <YAxis/>
       <CartesianGrid strokeDasharray="3 3"/>
       <Tooltip/>
       <Line type="monotone" dataKey="views" stroke="#8884d8" />
      </LineChart>
    );
  }
}


export class SimplePieChart extends React.Component{
	render () {
    var data = this.props.data
    var colors = this.props.colors

  	return (
    	<PieChart width={400} height={300} onMouseEnter={this.onPieEnter}>
        <Pie
          data={data}
          dataKey="value"
          cx={200}
          cy={150}
          labelLine={false}
          label={renderCustomizedLabel}
          outerRadius={100}
          fill="#8884d8"
        >
        	{
          	data.map((entry, index) => <Cell key={index}
              fill={colors[index % colors.length]}/>)
          }
        </Pie>
        <Tooltip/>
        <Legend/>
      </PieChart>
    );
  }
}
