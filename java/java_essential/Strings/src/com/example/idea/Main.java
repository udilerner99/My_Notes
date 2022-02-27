package com.example.idea;

public class Main {

    public static void main(String[] args) {
        var sb = new StringBuilder("welcome");
        sb.append(" to california");
        var s = sb.toString();
        StringBuilder b = new StringBuilder();
        b.append("Shirt size: ")
                .append("M")
                .append(", Qty: ")
                .append(4);
        var s2 = b.toString();
        System.out.println(s2);
    }
}
