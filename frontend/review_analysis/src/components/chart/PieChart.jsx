import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";
import { Box, Typography} from "@mui/material";

function PieChart({ positive, negative, neutral, title }) {
  const ref = useRef();

  useEffect(() => {
    const chart = new Chart(ref.current, {
      type: "doughnut",
      data: {
        labels: ["Позитивные", "Негативные", "Нейтральные"],
        datasets: [
          {
            data: [positive, negative, neutral],
            backgroundColor: ["#5ceda7ff", "#ff4b63ff", "#6948fcff"],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom", // Легенда внизу
          },
          title: {
            display: false, // Если хочешь использовать MUI Typography вместо встроенного Chart.js
          },
      },
    },
    });

    return () => chart.destroy();
  }, [positive, negative, neutral]);

  return (
    <Box width={500} height={550}  display="flex" flexDirection="column" alignItems="center">
        <Typography variant="h6" mb={2} margin="0" textAlign="center" fontSize={"24px"} fontWeight={"600"} fontFamily={"Montserrat"}>
          {title}
        </Typography>
    
      <Box width={500} height={500}>
        <canvas ref={ref} />
      </Box>
    </Box>
  );
}

export default PieChart;
