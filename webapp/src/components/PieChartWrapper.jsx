import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from 'recharts';

const shadesOfBlue = ["#4169E1", "#89CFF0", "#7393B3", "#7DF9FF"]

export default function PieChartWrapper({ chartData }) {
    return (
        <ResponsiveContainer width="100%" height="100%">
            <PieChart>
                <Pie data={chartData} cx="50%" cy="50%" label={({name}) => name} dataKey="value" nameKey="name">
                    {chartData.map((entry, index) => (
                        <Cell key={index} fill={shadesOfBlue[index % shadesOfBlue.length]} />
                    ))}
                </Pie>

                <Tooltip />
            </PieChart>
        </ResponsiveContainer>
    )
}