import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function BarChartWrapper({ chartData }) {
    return (
    <ResponsiveContainer>
        <BarChart data={chartData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" radius={[6, 6, 0, 0]}>
            {chartData.map((entry, index) => (
                <Cell key={index} fill={entry.color === 1 ? '#4169E1' : '#C0C0C0'} />
            ))}
            </Bar>
        </BarChart>
    </ResponsiveContainer>
    )
}