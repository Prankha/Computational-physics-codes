using Plots

function simulation()

    n = 1
    T = 1000

    lx, ly = 10.0, 10.0
    dx = lx / 10
    dy = ly / 10

    vx, vy = 2.0, 1.0

    dt = sqrt(dx^2 + dy^2) / (20 * sqrt(vx^2 + vy^2))

    p1, p2 = 5.0, 5.0

    x = Float64[]
    y = Float64[]

    anim = @animate for frame in 1:1000

        p1 += vx * dt
        p2 += vy * dt

        if p1 >= lx
            p1 = lx
            vx = -vx
        elseif p1 <= 0
            p1 = 0
            vx = -vx
        end

        if p2 >= ly
            p2 = ly
            vy = -vy
        elseif p2 <= 0
            p2 = 0
            vy = -vy
        end

        push!(x, p1)
        push!(y, p2)

        plot(
            x,
            y,
            xlim=(0, lx),
            ylim=(0, ly),
            aspect_ratio=:equal,
            xlabel="x",
            ylabel="y",
            legend=false,
            linewidth=1
        )

        plot!(
            [p1],
            [p2],
            seriestype=:scatter,
            markersize=5
        )

        plot!(
            [0, lx, lx, 0, 0],
            [0, 0, ly, ly, 0],
            color=:black,
            linewidth=1
        )
    end

    gif(anim, "particle_box.gif", fps=50)
end

simulation()