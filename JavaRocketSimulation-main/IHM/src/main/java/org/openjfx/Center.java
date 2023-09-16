package org.openjfx;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Center {
    public static ArrayList x = new ArrayList();
    public static ArrayList y = new ArrayList();

    public VBox center(){
        int i;
        for (i=0;i<25;i++){
            x.add(i);
            y.add(0);
        }
        VBox root = new VBox();
        root.setAlignment(Pos.CENTER);
        root.setPadding(new Insets(100));
        root.setSpacing(50);


        // Création du graphique.
        final NumberAxis xAxis = new NumberAxis(0, 3000,100 );
        xAxis.setLabel("Coût en millions d'euros");
        final NumberAxis yAxis = new NumberAxis(0, 100, 5);
        yAxis.setLabel("Pourcentage d'essais");
        final LineChart chart = new LineChart(xAxis, yAxis);
        chart.setTitle("Repartition des essais en fonction du coup");


        Button refresh = new Button("refresh");
        refresh.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent actionEvent) {
                final List<LineChart.Series> seriesList = new LinkedList<>();
                final int maxN = 1;
                final int minX = 0;
                final int maxX = 29;
                double minY = 0;
                double maxY = 0;
                for (int n = 0 ; n <= maxN ; n++) {
                    final LineChart.Series series  = new LineChart.Series<>();
                    series.setName(String.format("n = %d", n));
                    for (int x = 0 ; x <= maxX ; x++) {
                        final int value = (int)y.get(x)/1000;
                        minY = Math.min(minY, value);
                        maxY = Math.max(maxY, value);
                        final LineChart.Data data = new LineChart.Data(x*100, value);
                        series.getData().add(data);
                    }
                    seriesList.add(series);
                }

                chart.getData().setAll(seriesList);
                // Montage de l'IU.
            }


        });

        // Montage de l'IU.

        root.getChildren().add(chart);
        root.getChildren().add(refresh);

        return root;
    }
}
